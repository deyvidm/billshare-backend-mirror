from rest_framework import serializers

from app.bill.models import Bill
from app.transaction.serializers import TransactionSerializer


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['label', 'group', 'creator', 'total', 'currency_code', 'transactions']

    total = serializers.IntegerField(required=True, max_value=2147483647)
    currency_code = serializers.CharField(required=True, max_length=3, min_length=3)
    transactions = TransactionSerializer(many=True)
