from django.db.models import Sum
from rest_framework import serializers

from merger.models import TransactionLog, TransactionLogMerge, TransactionCategory, TransactionCategoryMatcher


class CreateTransactionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = ['date', 'description', 'account', 'category', 'amount']


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['id', 'name', 'variant']


class TransactionCategoryMatcherSerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer()

    class Meta:
        model = TransactionCategoryMatcher
        fields = ['id', 'regex_expression', 'category']


class TransactionLogSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    category = TransactionCategorySerializer()

    class Meta:
        model = TransactionLog
        fields = ['id', 'date', 'description', 'account', 'category', 'amount']

    @staticmethod
    def get_amount(instance):
        to_amount = TransactionLogMerge.objects.filter(
            to_transaction=instance
        ).aggregate(
            sum=Sum('amount', default=0)
        )['sum']

        from_amount = TransactionLogMerge.objects.filter(
            from_transaction=instance
        ).aggregate(
            sum=Sum('amount', default=0)
        )['sum']

        return instance.amount + to_amount - from_amount


class TransactionLogMergeSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(
        min_value=0,
    )

    def validate(self, data):
        from_transaction = data.get('from_transaction')

        attempted_amount_transfer = data.get('amount')
        available_amount = getattr(from_transaction, 'amount')

        if attempted_amount_transfer > available_amount:
            raise serializers.ValidationError(
                'Cannot transfer from transaction more than the available transaction value')

        return data

    class Meta:
        model = TransactionLogMerge
        fields = ['from_transaction', 'to_transaction', 'amount']
