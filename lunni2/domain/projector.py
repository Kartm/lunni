from datetime import date
from decimal import Decimal
import uuid
from collections import defaultdict

from .rules import RowCtx, matches_rule
from .types import EffectiveRow
from ..models import RawTransaction, DomainEvent, Category, CategorizationRule


def _parse_uuid(s: str) -> uuid.UUID:
    return uuid.UUID(s)


def build_effective_rows(
    *,
    start_date: date | None = None,
    end_date: date | None = None,
) -> tuple[list[EffectiveRow], dict[uuid.UUID, list[int]]]:
    """
    Returns:
      rows: list of group rows + ungrouped tx rows
      group_members: {group_id: [tx_id, ...]} for expand UI
    """

    tx_qs = RawTransaction.objects.all()
    if start_date:
        tx_qs = tx_qs.filter(date__gte=start_date)
    if end_date:
        tx_qs = tx_qs.filter(date__lte=end_date)
    # newest first; id tie-breaker for stable ordering
    txs = list(tx_qs.order_by("-date", "-id"))

    # replay only grouping events (fast enough for 10k)
    grouping_events = list(
        DomainEvent.objects.filter(
            type__in=[
                DomainEvent.Type.GROUP_CREATED,
                DomainEvent.Type.GROUP_RENAMED,
                DomainEvent.Type.GROUP_MEMBERS_ADDED,
                DomainEvent.Type.GROUP_MEMBERS_REMOVED,
            ]
        ).order_by("created_at", "id")
    )

    category_events = list(
        DomainEvent.objects.filter(
            type__in=[
                DomainEvent.Type.CATEGORY_ASSIGNED,
            ]
        ).order_by("created_at", "id")
    )

    group_title: dict[uuid.UUID, str] = {}
    group_currency: dict[uuid.UUID, str] = {}
    members: dict[uuid.UUID, set[int]] = defaultdict(set)

    # track membership tx_id -> group_id (enforce "at most one group" on read side)
    tx_to_group: dict[int, uuid.UUID] = {}

    for e in grouping_events:
        p = e.payload
        if e.type == DomainEvent.Type.GROUP_CREATED:
            gid = _parse_uuid(p["group_id"])
            group_title[gid] = p["title"]
            group_currency[gid] = p["currency"]
        elif e.type == DomainEvent.Type.GROUP_RENAMED:
            gid = _parse_uuid(p["group_id"])
            group_title[gid] = p["title"]
        elif e.type == DomainEvent.Type.GROUP_MEMBERS_ADDED:
            gid = _parse_uuid(p["group_id"])
            for tx_id in p.get("tx_ids", []):
                # if tx was in another group, remove it there (latest wins)
                if tx_id in tx_to_group and tx_to_group[tx_id] != gid:
                    old = tx_to_group[tx_id]
                    members[old].discard(tx_id)
                tx_to_group[tx_id] = gid
                members[gid].add(tx_id)
        elif e.type == DomainEvent.Type.GROUP_MEMBERS_REMOVED:
            gid = _parse_uuid(p["group_id"])
            for tx_id in p.get("tx_ids", []):
                if tx_to_group.get(tx_id) == gid:
                    tx_to_group.pop(tx_id, None)
                members[gid].discard(tx_id)

    # index tx by id for fast lookups
    tx_by_id = {t.id: t for t in txs}

    # build group rows
    group_rows: list[EffectiveRow] = []
    for gid, tx_ids_set in members.items():
        tx_ids = sorted(tx_ids_set)
        if not tx_ids:
            continue

        # enforce currency constraint at projection time too
        currency = group_currency.get(gid)
        if currency is None:
            # group exists only if created event exists; if missing, ignore
            continue

        member_txs = [tx_by_id[i] for i in tx_ids if i in tx_by_id]
        member_txs = [t for t in member_txs if t.currency == currency]
        if not member_txs:
            continue

        # net sum: expenses(neg) + repayments(pos)
        total = sum((t.amount for t in member_txs), Decimal("0.00"))

        # sorting date: choose max date (most recent activity in the group)
        date = max(t.date for t in member_txs)

        group_rows.append(
            EffectiveRow(
                kind="GROUP",
                row_id=f"group:{gid}",
                group_id=gid,
                date=date,
                description=group_title.get(gid, "Untitled group"),
                amount=total,
                currency=currency,
            )
        )

    valid_group_ids = {r.group_id for r in group_rows if r.group_id}

    # build ungrouped tx rows
    grouped_ids = {tx_id for tx_id, gid in tx_to_group.items() if gid in valid_group_ids}

    tx_rows = [
        EffectiveRow(
            kind="TX",
            row_id=f"tx:{t.id}",
            tx_id=t.id,
            date=t.date,
            description=t.description,
            amount=t.amount,
            currency=t.currency,
        )
        for t in txs
        if t.id not in grouped_ids
    ]

    # combine + sort globally (date desc, then kind to keep groups stable)
    rows = group_rows + tx_rows
    rows.sort(key=lambda r: (r.date, r.kind, r.row_id), reverse=True)

    ##### rules
    tx_category_override: dict[int, int] = {}
    group_category_override: dict[uuid.UUID, int] = {}

    for e in category_events:
        cat_id = e.payload.get("category_id")
        if not cat_id:
            continue

        if e.raw_transaction_id:
            tx_category_override[e.raw_transaction_id] = int(cat_id)
        if e.group_id:
            group_category_override[e.group_id] = int(cat_id)

    categories = {c.id: c for c in Category.objects.filter(deleted_at__isnull=True).order_by("name")}
    rules = list(
        CategorizationRule.objects.filter(deleted_at__isnull=True)
        .order_by("priority", "id")
        .select_related("target_category")
        .prefetch_related("conditions")
    )

    def _apply_category(row: EffectiveRow, category_id: int | None) -> EffectiveRow:
        if not category_id:
            return row.__class__(**{
                **row.__dict__,
                "category_css": "cat-none",
            })
        c = categories.get(category_id)
        if not c:
            return row.__class__(**{
            **row.__dict__,
            "category_css": "cat-none",
        })
        return row.__class__(**{
            **row.__dict__,
            "category_id": c.id,
            "category_name": c.name,
            "category_kind": c.kind,
            "category_css": f"cat-{c.kind.lower()}",
        })
    #####

    # return members mapping as list for expand UI
    group_members = {
        gid: sorted([tx_id for tx_id in tx_ids_set if tx_id in tx_by_id])
        for gid, tx_ids_set in members.items()
        if tx_ids_set and gid in valid_group_ids
    }

    # Apply categorization (after grouping)
    categorized_rows: list[EffectiveRow] = []
    for r in rows:
        cat_id = None

        if r.kind == "GROUP":
            # explicit override wins
            if r.group_id and r.group_id in group_category_override:
                cat_id = group_category_override[r.group_id]
            else:
                ctx = RowCtx(kind="GROUP", tx=None, group_id=str(r.group_id), group_title=r.description)
                for rule in rules:
                    if matches_rule(rule, ctx):
                        cat_id = rule.target_category_id
                        break

        else:  # TX
            if r.tx_id and r.tx_id in tx_category_override:
                cat_id = tx_category_override[r.tx_id]
            else:
                tx = tx_by_id.get(r.tx_id) if r.tx_id else None
                ctx = RowCtx(kind="TX", tx=tx, group_id=None, group_title=None)
                for rule in rules:
                    if matches_rule(rule, ctx):
                        cat_id = rule.target_category_id
                        break

        categorized_rows.append(_apply_category(r, cat_id))

    # hide ignored
    rows = [r for r in categorized_rows if r.category_kind != "IGN"]

    return rows, group_members
