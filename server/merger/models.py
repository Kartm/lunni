from django.db import models
from django.db.models import PositiveIntegerField, IntegerField
from django_extensions.db.models import TimeStampedModel


class TransactionCategoryMatcher(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    regex_expression = models.CharField(max_length=255)



class TransactionCategory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class CategoryVariant(models.TextChoices):
        POSITIVE = 'POS',
        NEGATIVE = 'NEG',
        IGNORE = 'IGN'

    variant = models.CharField(
        max_length=3,
        choices=CategoryVariant.choices,
        default=CategoryVariant.NEGATIVE,
    )

class TransactionLog(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    description = models.CharField(max_length=512)
    account = models.CharField(max_length=255)
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.RESTRICT,
        related_name='category_set',
        null=True
    )
    amount = IntegerField()


# todo order by date
# todo handle PKO files
# todo category positive negative

class TransactionLogMerge(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    from_transaction = models.ForeignKey(
        TransactionLog,
        on_delete=models.RESTRICT,
        related_name='merge_transaction_from_set',
    )
    to_transaction = models.ForeignKey(
        TransactionLog,
        on_delete=models.RESTRICT,
        related_name='merge_transaction_to_set',
    )
    amount = PositiveIntegerField()
