from collections import defaultdict
from datetime import date
from decimal import Decimal

from ..domain.projector import build_effective_rows


def build_monthly_category_breakdown(*, start_date=None, end_date=None):
    rows, _group_members = build_effective_rows(start_date=start_date, end_date=end_date)

    sums = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(Decimal))))

    for r in rows:
        if r.category_kind in ("POS", "NEG") and r.category_name:
            kind = r.category_kind
            category_name = r.category_name
        elif not r.category_kind and not r.category_name:
            kind = "POS" if r.amount >= 0 else "NEG"
            category_name = "Uncategorized"
        else:
            continue

        month_key = date(r.date.year, r.date.month, 1)
        sums[month_key][kind][category_name][r.currency] += r.amount

    months = []
    for month_key in sorted(sums.keys(), reverse=True):
        kinds = sums[month_key]
        months.append({
            "month": month_key,
            "month_label": month_key.strftime("%Y-%m"),
            "pos": _build_kind_breakdown(kinds.get("POS", {})),
            "neg": _build_kind_breakdown(kinds.get("NEG", {})),
        })

    return months


def _build_kind_breakdown(category_map):
    categories = []
    totals = defaultdict(Decimal)

    for cat_name in sorted(category_map.keys()):
        currency_map = category_map[cat_name]
        amounts = []
        for currency in sorted(currency_map.keys()):
            amount = currency_map[currency]
            amounts.append({"currency": currency, "amount": amount})
            totals[currency] += amount
        categories.append({"name": cat_name, "amounts": amounts})

    total_amounts = [
        {"currency": currency, "amount": totals[currency]}
        for currency in sorted(totals.keys())
    ]

    return {
        "categories": categories,
        "totals": total_amounts,
    }
