import datetime
import json
import uuid

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST

from ..domain.projector import build_effective_rows
from ..domain.types import Selection
from ..models import CategorizationRule, RuleCondition, RawTransaction, Category
from ..services.grouping import create_group, add_group_members, remove_group_members
from ..services.imports import import_transactions_csv
from ..services.selection import set_selection, clear_selection, get_selection


@require_POST
def upload_transactions_csv(request):
    f = request.FILES.get("file")
    if not f:
        return HttpResponseBadRequest("Missing file")

    stats = import_transactions_csv(f.file)

    response = render(
        request,
        "lunni2/partials/_upload_result.html",
        {"stats": stats},
    )
    response["HX-Trigger"] = json.dumps({"transactions-changed": stats})
    return response


@require_POST
def create_group_from_selection(request):
    title = (request.POST.get("title") or "").strip()
    if not title:
        return HttpResponseBadRequest("Missing title")

    sel = get_selection(request)
    if sel.group_ids:
        return HttpResponseBadRequest("Cannot create group when groups are selected.")
    if not sel.tx_ids:
        return HttpResponseBadRequest("Select transactions first.")

    gid = create_group(title=title, tx_ids=sorted(sel.tx_ids))

    clear_selection(request)

    resp = HttpResponse(status=204)
    resp["HX-Trigger"] = json.dumps({"transactions-changed": {"group_id": str(gid)}, "selection-changed": {}})
    return resp


@require_POST
def ungroup_member(request, group_id: uuid.UUID):
    tx_id = request.POST.get("tx_id")
    if not tx_id:
        return HttpResponseBadRequest("Missing tx_id")

    remove_group_members(group_id=group_id, tx_ids=[int(tx_id)])

    # figure out if group is now empty (so we can show a toast)
    rows, group_members_map = build_effective_rows()
    remaining = group_members_map.get(group_id) or []

    toast = "Removed from group."
    if len(remaining) == 0:
        toast = "Group dissolved (no members left)."

    resp = render(request, "lunni2/partials/_action_result.html", {
        "text": toast
    })
    resp["HX-Trigger"] = json.dumps({"transactions-changed": {}})
    return resp


@require_POST
def add_selection_to_group(request):
    sel = get_selection(request)
    if len(sel.group_ids) != 1:
        return HttpResponseBadRequest("Select exactly one group.")
    if not sel.tx_ids:
        return HttpResponseBadRequest("Select transactions to add.")

    gid = next(iter(sel.group_ids))
    add_group_members(group_id=gid, tx_ids=sorted(sel.tx_ids))

    clear_selection(request)

    resp = HttpResponse(status=204)
    resp["HX-Trigger"] = json.dumps({"transactions-changed": {}, "selection-changed": {}})
    return resp

@require_POST
def merge_selection_into_new_group(request):
    title = (request.POST.get("title") or "").strip()
    if not title:
        return HttpResponseBadRequest("Missing title")

    sel = get_selection(request)
    if len(sel.group_ids) < 2:
        return HttpResponseBadRequest("Select at least two groups to merge.")

    rows, group_members_map = build_effective_rows()

    merged_tx_ids = set(sel.tx_ids)
    for gid in sel.group_ids:
        merged_tx_ids.update(group_members_map.get(gid, []))

    gid = create_group(title=title, tx_ids=sorted(merged_tx_ids))

    clear_selection(request)

    resp = HttpResponse(status=204)
    resp["HX-Trigger"] = json.dumps({"transactions-changed": {"group_id": str(gid)}, "selection-changed": {}})
    return resp


@require_POST
def toggle_selection(request):
    kind = request.POST.get("kind")  # "tx" or "group"
    raw_id = request.POST.get("id")
    if kind not in ("tx", "group") or not raw_id:
        return HttpResponseBadRequest("Missing kind/id")

    sel = get_selection(request)

    if kind == "tx":
        tx_id = int(raw_id)
        tx_ids = set(sel.tx_ids)
        if tx_id in tx_ids:
            tx_ids.remove(tx_id)
        else:
            tx_ids.add(tx_id)
        sel = Selection(tx_ids=tx_ids, group_ids=set(sel.group_ids))

    else:  # group
        gid = uuid.UUID(raw_id)
        group_ids = set(sel.group_ids)
        if gid in group_ids:
            group_ids.remove(gid)
        else:
            group_ids.add(gid)
        sel = Selection(tx_ids=set(sel.tx_ids), group_ids=group_ids)

    set_selection(request, sel)

    resp = HttpResponse(status=204)
    resp["HX-Trigger"] = json.dumps({"selection-changed": {}})
    return resp


@require_POST
def clear_selection_action(request):
    clear_selection(request)
    resp = HttpResponse(status=204)
    resp["HX-Trigger"] = json.dumps({"selection-changed": {}})
    return resp



@require_POST
def create_rule_action(request):
    name = (request.POST.get("name") or "").strip() or "Rule"
    priority = int(request.POST.get("priority") or "100")
    category_id = request.POST.get("category_id")

    field = request.POST.get("field") or "description"
    op = request.POST.get("op") or "contains"
    value = (request.POST.get("value") or "").strip()

    if not category_id:
        return HttpResponseBadRequest("Missing category_id")
    if not value:
        return HttpResponseBadRequest("Missing rule value")

    rule = CategorizationRule.objects.create(
        name=name,
        priority=priority,
        target_category_id=int(category_id),
    )
    RuleCondition.objects.create(
        rule=rule,
        field=field,
        operator=op,
        value=value,
    )

    resp = render(request, "lunni2/partials/_action_result.html", {
        "text": f"Saved rule: {name}",
    })
    resp["HX-Trigger"] = json.dumps({"transactions-changed": {}})
    return resp

@require_POST
def categorize_selection_action(request):
    category_id = request.POST.get("category_id")
    if not category_id:
        return HttpResponseBadRequest("Missing category_id")
    category_id = int(category_id)

    sel = get_selection(request)

    # TX manual rules via fingerprint equals
    txs = list(RawTransaction.objects.filter(id__in=sel.tx_ids))
    for tx in txs:
        r = CategorizationRule.objects.create(
            name=f"Manual TX: {tx.description[:40]}",
            priority=0,
            target_category_id=category_id,
        )
        RuleCondition.objects.create(
            rule=r,
            field=RuleCondition.Field.FINGERPRINT,
            operator=RuleCondition.Operator.EQUALS,
            value=tx.fingerprint,
        )

    # GROUP manual rules via group_id equals (string uuid)
    for gid in sel.group_ids:
        r = CategorizationRule.objects.create(
            name=f"Manual GROUP: {gid}",
            priority=0,
            target_category_id=category_id,
        )
        RuleCondition.objects.create(
            rule=r,
            field=RuleCondition.Field.GROUP_ID,
            operator=RuleCondition.Operator.EQUALS,
            value=str(gid),
        )

    # optional: clear selection after applying
    clear_selection(request)

    resp = render(request, "lunni2/partials/_action_result.html", {
        "text": "Categorized selection.",
    })
    resp["HX-Trigger"] = json.dumps({
        "transactions-changed": {},
        "selection-changed": {"count": 0, "action": "cleared"},
    })
    return resp

@require_POST
def create_category_action(request):
    name = (request.POST.get("name") or "").strip()
    kind = (request.POST.get("kind") or "").strip()

    if not name:
        return HttpResponseBadRequest("Missing name")
    if kind not in [Category.Kind.POS, Category.Kind.NEG, Category.Kind.IGN]:
        return HttpResponseBadRequest("Invalid kind")

    # prevent duplicates among active categories
    exists = Category.objects.filter(name=name, deleted_at__isnull=True).exists()
    if exists:
        return HttpResponseBadRequest("Category name already exists")

    Category.objects.create(name=name, kind=kind)

    resp = render(request, "lunni2/partials/_action_result.html", {"text": "Category created."})
    resp["HX-Trigger"] = json.dumps({"categories-changed": {}, "transactions-changed": {}})
    return resp


@require_POST
def delete_category_action(request, category_id: int):
    cat = Category.objects.filter(id=category_id, deleted_at__isnull=True).first()
    if not cat:
        return HttpResponseBadRequest("Category not found")

    # soft delete
    cat.deleted_at = datetime.datetime.now()
    cat.save(update_fields=["deleted_at"])

    resp = render(request, "lunni2/partials/_action_result.html", {"text": f"Category deleted: {cat.name}"})
    resp["HX-Trigger"] = json.dumps({"categories-changed": {}, "transactions-changed": {}})
    return resp