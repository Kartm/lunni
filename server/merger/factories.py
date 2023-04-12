import factory


class TransactionLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'merger.TransactionLog'

    date = '2023-01-05'
    description = 'desc'
    account = 'prywatnte'
    category = None
    amount = 1
