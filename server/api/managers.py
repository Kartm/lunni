from django.db import models
from django.db.models import F, Sum, Q
from django.db.models.functions import Coalesce


class TransactionsMergedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            # finds all related transaction merges
            calculated_amount=
            F('amount') -
            Coalesce(
                # sum of all merges where some amount is 'lost' from this transaction
                Sum('frommerge__amount', filter=Q(frommerge__from_transaction=F('id'))),
                0
            ) +
            Coalesce(
                # sum of all merges where some amount is 'gained' to this transaction
                Sum('tomerge__amount', filter=Q(tomerge__to_transaction=F('id'))),
                0
            )
        ).exclude(calculated_amount__exact=0).exclude(category__variant__exact='IGN').order_by('-date', 'amount')
