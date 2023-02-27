from rest_framework import serializers

from files.models import Entry


class EntrySerializer(serializers.ModelSerializer):
    amount = serializers.FloatField()

    class Meta:
        model = Entry
        fields = ['id', 'date', 'description', 'account', 'category', 'amount']
