import uuid

from lunni2.domain.types import Selection


def get_selection(request) -> Selection:
    raw = request.session.get("selection", {"tx_ids": [], "group_ids": []})
    tx_ids = set(map(int, raw.get("tx_ids", [])))
    group_ids = set(uuid.UUID(x) for x in raw.get("group_ids", []))
    return Selection(tx_ids=tx_ids, group_ids=group_ids)

def set_selection(request, sel: Selection) -> None:
    request.session["selection"] = {
        "tx_ids": sorted(sel.tx_ids),
        "group_ids": sorted(str(g) for g in sel.group_ids),
    }
    request.session.modified = True

def clear_selection(request) -> None:
    request.session["selection"] = {"tx_ids": [], "group_ids": []}
    request.session.modified = True