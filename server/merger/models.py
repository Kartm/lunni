from django.db import models
from django.db.models import PositiveIntegerField, IntegerField, UniqueConstraint
from django_extensions.db.models import TimeStampedModel

from merger.managers import TransactionLogManager


class TransactionCategory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class CategoryVariant(models.TextChoices):
        POSITIVE = 'POS',
        NEGATIVE = 'NEG',
        IGNORE = 'IGN'

    variant = models.CharField(
        max_length=3,
        choices=CategoryVariant.choices,
        default=CategoryVariant.NEGATIVE,
    )

    def __str__(self):
        return '({}) {}, {}'.format(self.id, self.name, self.variant)


class TransactionCategoryMatcher(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    regex_expression = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.RESTRICT,
        related_name='category_matcher_set',
        null=True
    )

    def __str__(self):
        return '({}) <{}>, {}'.format(self.id, self.regex_expression, self.category.name)


class TransactionLog(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    description = models.CharField(max_length=512)
    account = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.RESTRICT,
        related_name='transaction_log_set',
        null=True
    )
    amount = IntegerField()
    objects = TransactionLogManager()

    def __str__(self):
        return '({}) {}, {}, {}, {}'.format(self.id, self.date, self.category, self.note, self.description)

    class Meta:
        # TODO short-term fix, improves upload time from 47s -> 40s
        indexes = [
            models.Index(fields=['date', 'description', 'account', 'amount']),
        ]


class TransactionLogMerge(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    from_transaction = models.ForeignKey(
        TransactionLog,
        on_delete=models.RESTRICT,
        related_name='frommerge',
    )
    to_transaction = models.ForeignKey(
        TransactionLog,
        on_delete=models.RESTRICT,
        related_name='tomerge',
    )
    amount = PositiveIntegerField()

    def __str__(self):
        return '({}) {} -> {}, {}'.format(self.id, self.from_transaction.description, self.to_transaction.description,
                                          self.amount)
