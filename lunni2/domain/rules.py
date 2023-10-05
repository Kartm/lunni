from dataclasses import dataclass
from typing import Iterable

from lunni2.models import CategorizationRule, RuleCondition, RawTransaction

@dataclass(frozen=True)
class RowCtx:
    kind: str                    # "TX" or "GROUP"
    tx: RawTransaction | None    # TX row only
    group_id: str | None         # GROUP row only (string uuid)
    group_title: str | None

def _norm(s: str) -> str:
    return " ".join((s or "").strip().lower().split())

def matches_condition(cond: RuleCondition, ctx: RowCtx) -> bool:
    v = cond.value

    if cond.field == RuleCondition.Field.DESCRIPTION:
        if not ctx.tx: return False
        hay = _norm(ctx.tx.description)
        if cond.operator == RuleCondition.Operator.CONTAINS:
            return _norm(v) in hay
        return False

    if cond.field == RuleCondition.Field.FINGERPRINT:
        if not ctx.tx: return False
        if cond.operator == RuleCondition.Operator.EQUALS:
            return ctx.tx.fingerprint == v
        return False

    if cond.field == RuleCondition.Field.GROUP_ID:
        if ctx.kind != "GROUP": return False
        if cond.operator == RuleCondition.Operator.EQUALS:
            return (ctx.group_id or "") == v
        return False

    if cond.field == RuleCondition.Field.GROUP_TITLE:
        if ctx.kind != "GROUP": return False
        if cond.operator == RuleCondition.Operator.CONTAINS:
            return _norm(v) in _norm(ctx.group_title or "")
        return False

    return False


def matches_category_sign(*, category_kind: str, ctx: RowCtx) -> bool:
    # IGN applies to anything (recommended)
    if category_kind == "IGN":
        return True

    if not ctx.kind == "TX":
        # only use this for transactions
        return False

    if not ctx.tx:
        # should never happen
        return False

    # Zero matches nothing (safe default)
    if ctx.tx.amount.is_zero():
        return False

    if category_kind == "NEG":
        return ctx.tx.amount < 0
    if category_kind == "POS":
        return ctx.tx.amount > 0

    # Unknown kind: be safe
    return False

def matches_rule(rule: CategorizationRule, ctx: RowCtx) -> bool:
    conds = list(rule.conditions.all())
    if not matches_category_sign(category_kind=rule.target_category.kind, ctx=ctx):
        return False
    return all(matches_condition(c, ctx) for c in conds)