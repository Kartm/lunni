from django.db import models
from django.db.models import PositiveIntegerField, IntegerField


class TransactionLog(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    description = models.CharField(max_length=512)
    account = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    amount = IntegerField()


class TransactionLogMerge(models.Model):
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
