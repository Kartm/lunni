from ..models import RawTransaction, CategorizationRule, RuleCondition


def create_manual_tx_rule(*, tx: RawTransaction, category_id: int) -> CategorizationRule:
    r = CategorizationRule.objects.create(
        name=f"Manual: {tx.description[:40]}",
        priority=0,
        target_category_id=category_id,
    )
    RuleCondition.objects.create(
        rule=r,
        field=RuleCondition.Field.FINGERPRINT,
        operator=RuleCondition.Operator.EQUALS,
        value=tx.fingerprint,
    )
    return r