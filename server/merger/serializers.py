from rest_framework import serializers

from merger.models import PlainTransaction


class PlainTransactionSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField()

    class Meta:
        model = PlainTransaction
        fields = ['id', 'date', 'description', 'account', 'category', 'amount']
