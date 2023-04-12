import factory


class TransactionCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'merger.TransactionCategory'

    name = 'food'


class TransactionLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'merger.TransactionLog'

    date = '2023-01-05'
    description = 'desc'
    account = 'prywatnte'
    category = factory.SubFactory(TransactionCategoryFactory)
    amount = 1
