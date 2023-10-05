from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RawTransaction(TimestampedModel):
    date = models.DateField()
    description = models.TextField()
    this_account_number = models.CharField(max_length=64)
    other_account_name = models.CharField(max_length=255, blank=True, null=True)
    other_account_number = models.CharField(max_length=64, blank=True, null=True)

    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3)  # ISO-4217 (PLN/EUR)

    # Stable, deterministic fingerprint used for de-duplication
    fingerprint = models.CharField(max_length=64, unique=True)

    # keep original in case ever needed
    raw_payload = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["fingerprint"],
                name="uniq_fingerprint",
            ),
        ]


class Category(TimestampedModel):
    class Kind(models.TextChoices):
        POS = "POS", "Positive"
        NEG = "NEG", "Expense"
        IGN = "IGN", "Ignore"

    name = models.CharField(max_length=64, unique=True)
    kind = models.CharField(max_length=3, choices=Kind.choices)

    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class CategorizationRule(TimestampedModel):
    name = models.CharField(max_length=128)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # todo manual rules have very high priority
    priority = models.PositiveIntegerField(default=100)

    target_category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="rules"
    )

    class Meta:
        indexes = [
            models.Index(fields=["priority"]),
        ]

    def __str__(self) -> str:
        return f"[{self.priority}] {self.name}"

class RuleCondition(models.Model):
    class Field(models.TextChoices):
        DESCRIPTION = "description", "Description" # tx
        FINGERPRINT = "fingerprint", "Fingerprint" # tx
        GROUP_ID = "group_id", "Group ID" # group
        GROUP_TITLE = "group_title", "Group title" # group

    class Operator(models.TextChoices):
        CONTAINS = "contains", "contains"
        EQUALS = "equals", "equals"  # used for fingerprint == X in manual rules

    rule = models.ForeignKey(
        CategorizationRule, on_delete=models.CASCADE, related_name="conditions"
    )
    field = models.CharField(max_length=32, choices=Field.choices)
    operator = models.CharField(max_length=16, choices=Operator.choices)
    value = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["field", "operator"]),
        ]

    def __str__(self) -> str:
        return f"{self.field} {self.operator} {self.value}"


class DomainEvent(TimestampedModel):
    """
    Append-only event log. This is the “truth” of changes.
    Rebuild projections by replaying events in created_at order (and tie-break by id).
    """
    class Type(models.TextChoices):
        NOTE_SET = "NOTE_SET", "Note set"
        CATEGORY_ASSIGNED = "CATEGORY_ASSIGNED", "Category assigned"
        RULE_CREATED = "RULE_CREATED", "Rule created"
        RULE_DELETED = "RULE_DELETED", "Rule deleted"

        GROUP_CREATED = "GROUP_CREATED", "Group created"
        GROUP_RENAMED = "GROUP_RENAMED", "Group renamed"
        GROUP_MEMBERS_ADDED = "GROUP_MEMBERS_ADDED", "Group members added"
        GROUP_MEMBERS_REMOVED = "GROUP_MEMBERS_REMOVED", "Group members removed"

    type = models.CharField(max_length=48, choices=Type.choices)

    # stream_key lets you partition events:
    #   raw_tx:<id>, group:<uuid>, rules, etc.
    stream_key = models.CharField(max_length=128)

    # Store event data (ids, amounts, rate ids, etc.)
    payload = models.JSONField(default=dict)

    raw_transaction = models.ForeignKey(RawTransaction, null=True, blank=True, on_delete=models.CASCADE)
    group_id = models.UUIDField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["stream_key", "created_at"]),
            models.Index(fields=["type", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.created_at:%Y-%m-%d %H:%M:%S} {self.type} [{self.stream_key}]"
