from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
import uuid

from lunni2.domain.types import SelectedItem, SelectionSummary
from lunni2.models import RawTransaction
from lunni2.domain.projector import build_effective_rows  # must include group rows with title/amount/currency



def build_selection_summary(*, tx_ids: set[int], group_ids: set[uuid.UUID]) -> SelectionSummary:
    items: list[SelectedItem] = []
    errors: list[str] = []

    # TX items
    txs = list(RawTransaction.objects.filter(id__in=tx_ids))
    tx_by_id = {t.id: t for t in txs}
    for tx_id in sorted(tx_ids):
        t = tx_by_id.get(tx_id)
        if not t:
            continue
        items.append(SelectedItem(
            kind="tx",
            id=str(tx_id),
            label=t.description,
            amount=t.amount,
            currency=t.currency,
        ))

    # GROUP items: take from projector
    rows, _ = build_effective_rows()
    group_row_by_id = {r.group_id: r for r in rows if r.kind == "GROUP"}

    for gid in sorted(group_ids, key=lambda x: str(x)):
        r = group_row_by_id.get(gid)
        if not r:
            continue
        items.append(SelectedItem(
            kind="group",
            id=str(gid),
            label=r.description,
            amount=r.amount,
            currency=r.currency,
        ))

    currencies = sorted({it.currency for it in items})
    currency = currencies[0] if len(currencies) == 1 else None

    total = None
    if currency is None and items:
        errors.append("Selected items contain multiple currencies. Actions disabled for now.")
    elif currency:
        total = sum((it.amount for it in items), Decimal("0.00"))

    G = len(group_ids)
    T = len(tx_ids)
    mode = "NONE"
    add_to_group_name = None

    if G == 0 and T > 0:
        mode = "CREATE_GROUP"
    elif G == 1 and T > 0:
        mode = "ADD_TO_GROUP"
        only_gid = next(iter(group_ids))
        gr = group_row_by_id.get(only_gid)
        add_to_group_name = gr.description if gr else "group"
    elif G >= 2:
        mode = "MERGE_ALL"

    return SelectionSummary(
        items=items,
        total=total,
        currency=currency,
        tx_count=T,
        group_count=G,
        mode=mode,
        add_to_group_name=add_to_group_name,
        errors=errors,
    )
