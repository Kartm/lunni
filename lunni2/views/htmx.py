from dataclasses import dataclass
from datetime import date
from urllib.parse import urlencode
from uuid import UUID

from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from ..domain.projector import build_effective_rows
from ..domain.rules import matches_rule, RowCtx
from ..models import RawTransaction, Category, RuleCondition
from ..services.selection import get_selection
from ..services.selection_summary import build_selection_summary


@require_GET
def transactions_table(request):
    page_number = request.GET.get("page", "1")
    start_date, end_date, only_uncategorized, querystring = _extract_filters(request)
    rows, _group_members = build_effective_rows(start_date=start_date, end_date=end_date)

    if only_uncategorized:
        rows = [r for r in rows if not r.category_id]

    paginator = Paginator(rows, 100)
    page_obj = paginator.get_page(page_number)

    sel = get_selection(request)

    resp = render(request, "lunni2/partials/_transactions_table.html", {
        "page_obj": page_obj,
        "selected_tx_ids": sel.tx_ids,
        "selected_group_ids": sel.group_ids,
        "start_date": start_date.isoformat() if start_date else "",
        "end_date": end_date.isoformat() if end_date else "",
        "only_uncategorized": only_uncategorized,
        "querystring": querystring,
    })
    params: dict[str, str] = {}
    if start_date:
        params["start_date"] = start_date.isoformat()
    if end_date:
        params["end_date"] = end_date.isoformat()
    if only_uncategorized:
        params["only_uncategorized"] = "1"
    if page_number and page_number != "1":
        params["page"] = str(page_number)

    push_url = reverse("transactions")
    if params:
        push_url = f"{push_url}?{urlencode(params)}"
    resp["HX-Push-Url"] = push_url
    return resp


@require_GET
def group_expand(request, group_id):
    # render toggle as expanded (▾) and load members via htmx "load"
    _start_date, _end_date, _only_uncategorized, querystring = _extract_filters(request)
    return render(
        request,
        "lunni2/partials/_group_toggle_expanded.html",
        {"group_id": group_id, "querystring": querystring},
    )


@require_GET
def group_collapse(request, group_id):
    # render toggle as collapsed (▸) and also clear members
    _start_date, _end_date, _only_uncategorized, querystring = _extract_filters(request)
    resp = render(
        request,
        "lunni2/partials/_group_toggle_collapsed.html",
        {"group_id": group_id, "querystring": querystring},
    )
    return resp


@require_GET
def group_members(request, group_id: UUID):
    """
    Returns the expandable content (member tx list) for a given group.
    """
    start_date, end_date, _only_uncategorized, _querystring = _extract_filters(request)
    rows, group_members_map = build_effective_rows(start_date=start_date, end_date=end_date)
    tx_ids = group_members_map.get(group_id, [])
    # newest first; id tie-breaker for stable ordering
    txs = list(RawTransaction.objects.filter(id__in=tx_ids).order_by("-date", "-id"))

    return render(
        request,
        "lunni2/partials/_group_members.html",
        {"group_id": group_id, "txs": txs},
    )


@require_GET
def selection_bar(request):
    sel = get_selection(request)
    summary = build_selection_summary(tx_ids=sel.tx_ids, group_ids=sel.group_ids)
    return render(request, "lunni2/partials/_selection_bar.html", {"s": summary})

def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None

def _extract_filters(request):
    start_date = _parse_date(request.GET.get("start_date"))
    end_date = _parse_date(request.GET.get("end_date"))
    only_uncategorized = request.GET.get("only_uncategorized") == "1"
    params: dict[str, str] = {}
    if start_date:
        params["start_date"] = start_date.isoformat()
    if end_date:
        params["end_date"] = end_date.isoformat()
    if only_uncategorized:
        params["only_uncategorized"] = "1"
    return start_date, end_date, only_uncategorized, urlencode(params)

@require_GET
def categorize_panel(request):
    rows, _ = build_effective_rows()

    uncat_count = sum(1 for r in rows if not r.category_id)
    sel = get_selection(request)

    categories = Category.objects.filter(deleted_at__isnull=True).order_by("name")

    return render(request, "lunni2/partials/_categorize_panel.html", {
        "uncat_count": uncat_count,
        "has_selection": bool(sel.tx_ids or sel.group_ids),
        "categories": categories,
    })

@require_GET
def categorize_preview(request):
    # minimal "conditions manager" shim that supports .all()
    class _CondList:
        def __init__(self, conds):
            self._conds = conds

        def all(self):
            return self._conds

    @dataclass(frozen=True)
    class _PreviewCond:
        field: str
        operator: str
        value: str

    @dataclass(frozen=True)
    class _PreviewTargetCategory:
        id: int
        kind: str  # "NEG" / "POS" / "IGN"
        name: str | None = None

    class _PreviewRule:
        def __init__(self, *, target_category: _PreviewTargetCategory, conditions: list[_PreviewCond]):
            self.target_category = target_category
            self.target_category_id = target_category.id
            self.conditions = _CondList(conditions)

    field = request.GET.get("field") or "description"
    op = request.GET.get("op") or "contains"
    value = (request.GET.get("value") or "").strip()

    target_category_id = request.GET.get("category_id")

    # default empty
    matches = []

    # need both value and category to evaluate sign gating
    if value and target_category_id:
        cat = Category.objects.filter(id=int(target_category_id), deleted_at__isnull=True).first()
        if cat:
            # Build preview conditions using the same enums your matcher expects
            if field == "description" and op == "contains":
                conds = [_PreviewCond(
                    field=RuleCondition.Field.DESCRIPTION,
                    operator=RuleCondition.Operator.CONTAINS,
                    value=value,
                )]
            elif field == "group_title" and op == "contains":
                conds = [_PreviewCond(
                    field=RuleCondition.Field.GROUP_TITLE,
                    operator=RuleCondition.Operator.CONTAINS,
                    value=value,
                )]
            else:
                conds = []

            if conds:
                preview_rule = _PreviewRule(
                    target_category=_PreviewTargetCategory(id=cat.id, kind=cat.kind, name=cat.name),
                    conditions=conds,
                )

                # IMPORTANT for option B: do NOT inject preview_rule into build_effective_rows
                rows, _ = build_effective_rows()

                # workflow constraint: only uncategorized
                candidates = [r for r in rows if not r.category_id]

                # We must be able to build RowCtx for TX rows (needs RawTransaction)
                tx_ids = [r.tx_id for r in candidates if r.kind == "TX" and r.tx_id]
                tx_by_id = {
                    t.id: t
                    for t in RawTransaction.objects.filter(id__in=tx_ids)
                }

                for r in candidates:
                    if r.kind == "GROUP":
                        ctx = RowCtx(
                            kind="GROUP",
                            tx=None,
                            group_id=str(r.group_id),
                            group_title=r.description,
                        )
                    else:
                        ctx = RowCtx(
                            kind="TX",
                            tx=tx_by_id.get(r.tx_id),
                            group_id=None,
                            group_title=None,
                        )

                    if matches_rule(preview_rule, ctx):
                        matches.append(r)

    return render(request, "lunni2/partials/_categorize_preview.html", {
        "matches": matches[:200],  # safety cap
        "count": len(matches),
        "value": value,
        "field": field,
        "op": op,
        "category_id": target_category_id,
    })

@require_GET
def categories_panel(request):
    categories = Category.objects.filter(deleted_at__isnull=True).order_by("name")
    return render(request, "lunni2/partials/_categories_panel.html", {"categories": categories})
