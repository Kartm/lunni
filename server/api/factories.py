import factory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.Category'

    name = 'food'
    variant = 'NEG'


class CategoryMatcherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.CategoryMatcher'

    regex_expression = 'des'
    category = factory.SubFactory(CategoryFactory)


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.Transaction'

    date = '2023-01-05'
    description = 'desc'
    account = 'prywatnte'
    category = factory.SubFactory(CategoryFactory)
    amount = 1
