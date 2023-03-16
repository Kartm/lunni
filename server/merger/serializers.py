from django.db.models import Sum
from rest_framework import serializers

from merger.models import TransactionLog, TransactionLogMerge


class CreateTransactionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = ['date', 'description', 'account', 'category', 'amount']


class TransactionLogSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

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

    class Meta:
        model = TransactionLogMerge
        fields = ['from_transaction', 'to_transaction', 'amount']

