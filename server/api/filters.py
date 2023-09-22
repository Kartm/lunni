import django_filters

from api.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='name')
    uncategorized = django_filters.BooleanFilter(field_name='category', lookup_expr='isnull')

    class Meta:
        model = Transaction
        fields = ['category']
