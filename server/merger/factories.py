import factory


class TransactionCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'merger.TransactionCategory'

    name = 'food'
    variant = 'NEG'


class TransactionCategoryMatcherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'merger.TransactionCategoryMatcher'

    regex_expression = 'des'
    category = factory.SubFactory(TransactionCategoryFactory)


class TransactionLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'merger.TransactionLog'

    date = '2023-01-05'
    description = 'desc'
    account = 'prywatnte'
    category = factory.SubFactory(TransactionCategoryFactory)
    amount = 1
