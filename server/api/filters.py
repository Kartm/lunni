import django_filters
from django_filters import DateFromToRangeFilter

from api.models import Transaction, Category

# allows to filter by a list (even if one of elements is not valid), allows to filter by category OR uncategorized
class CustomField(django_filters.fields.ModelMultipleChoiceField):
    def _check_values(self, value):
        """
        Override the base class' _check_values method so our queryset is not
        empty if one of the items in value is invalid.
        """
        null = self.null_label is not None and value and self.null_value in value
        if null:
            value = [v for v in value if v != self.null_value]
        field_name = self.to_field_name or 'pk'
        result = list(self.queryset.filter(**{'{}__in'.format(field_name): value}))
        result += [self.null_value] if null else []
        return result


class CustomModelMultipleChoiceFilter(django_filters.ModelMultipleChoiceFilter):
    field_class = CustomField


class TransactionFilter(django_filters.FilterSet):
    category = CustomModelMultipleChoiceFilter(
        field_name='category__name',
        to_field_name='name',
        null_label='None', # todo maybe can use ModelMultipleChoiceFilter. but why these two have to be filled...
        null_value='None',
        queryset=Category.objects.all(),
        conjoined=False
    )

    date = DateFromToRangeFilter()

    class Meta:
        model = Transaction
        fields = ['category', 'date']
