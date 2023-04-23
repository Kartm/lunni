from django.db import models
from django.db.models import F, Sum, Q
from django.db.models.functions import Coalesce


class TransactionLogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            calculated_amount=
            F('amount') -
            Coalesce(
                Sum('frommerge__amount', filter=Q(frommerge__from_transaction=F('id'))),
                0
            ) +
            Coalesce(
                Sum('tomerge__amount', filter=Q(tomerge__to_transaction=F('id'))),
                0
            )
        ).exclude(calculated_amount__exact=0).order_by('-date', 'amount')
