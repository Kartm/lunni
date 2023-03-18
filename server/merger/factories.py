import factory

from merger.models import TransactionLog


class TransactionLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'merger.TransactionLog'

    date = '2023-01-05'
    description = 'desc'
    account = 'prywatnte'
    category = 'lol wydatkii'
    amount = 1
