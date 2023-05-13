from django.db import models
from django.db.models import PositiveIntegerField, IntegerField
from django_extensions.db.models import TimeStampedModel

from api.managers import TransactionsMergedManager


class Category(TimeStampedModel):
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

    class Meta:
        indexes = [
            # speeds up fetching, they are ordered in a view by DESC created date
            models.Index(fields=['-created']),
        ]


class CategoryMatcher(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    regex_expression = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        related_name='category_matcher_set',
        null=True
    )

    def __str__(self):
        return '({}) <{}>, {}'.format(self.id, self.regex_expression, self.category.name)

    class Meta:
        indexes = [
            # speeds up fetching, they are ordered in a view by DESC created date
            models.Index(fields=['-created']),
        ]


class Transaction(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    description = models.CharField(max_length=512)
    account = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        related_name='transaction_log_set',
        null=True
    )
    amount = IntegerField()

    # prevent records with calculated_amount=0 from being hidden in Django admin
    admin_objects = models.Manager()
    objects = TransactionsMergedManager()

    def __str__(self):
        return '({}) {}, {}, {}, {}'.format(self.id, self.date, self.category, self.note, self.description)

    class Meta:
        indexes = [
            # improves upload time because we during upload we search for duplicates
            models.Index(fields=['date', 'description', 'account', 'amount']),
            # improves fetching pages of transactions because we sort them by these fields
            models.Index(fields=['-date', 'amount']),
        ]


class TransactionMerge(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    from_transaction = models.ForeignKey(
        Transaction,
        on_delete=models.RESTRICT,
        related_name='frommerge',
    )
    to_transaction = models.ForeignKey(
        Transaction,
        on_delete=models.RESTRICT,
        related_name='tomerge',
    )
    amount = PositiveIntegerField()

    def __str__(self):
        return '({}) {} -> {}, {}'.format(self.id, self.from_transaction.description, self.to_transaction.description,
                                          self.amount)
