from datetime import date
from urllib.parse import urlencode

from django.shortcuts import render
from django.views.decorators.http import require_GET

from ..services.breakdowns import build_monthly_category_breakdown


@require_GET
def transactions_page(request):
    start_date = _parse_date(request.GET.get("start_date"))
    end_date = _parse_date(request.GET.get("end_date"))
    only_uncategorized = request.GET.get("only_uncategorized") == "1"
    page = request.GET.get("page") or "1"

    params: dict[str, str] = {}
    if start_date:
        params["start_date"] = start_date.isoformat()
    if end_date:
        params["end_date"] = end_date.isoformat()
    if only_uncategorized:
        params["only_uncategorized"] = "1"
    querystring = urlencode(params)

    return render(request, "lunni2/pages/transactions.html", {
        "start_date": start_date.isoformat() if start_date else "",
        "end_date": end_date.isoformat() if end_date else "",
        "only_uncategorized": only_uncategorized,
        "page": page,
        "querystring": querystring,
    })


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


@require_GET
def breakdown_page(request):
    start_date = _parse_date(request.GET.get("start_date"))
    end_date = _parse_date(request.GET.get("end_date"))

    months = build_monthly_category_breakdown(
        start_date=start_date,
        end_date=end_date,
    )

    return render(request, "lunni2/pages/breakdown.html", {
        "months": months,
        "start_date": start_date.isoformat() if start_date else "",
        "end_date": end_date.isoformat() if end_date else "",
    })
