from rest_framework import serializers

from app.bill.models import Bill
from app.transaction.serializers import TransactionOperationSerializer


class TransactionOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['label', 'group', 'creator', 'total', 'currency_code', 'transactions']

    total = serializers.DecimalField(required=True, decimal_places=2, max_digits=100)
    currency_code = serializers.CharField(required=True, max_length=3, min_length=3)
    transactions = TransactionOperationSerializer(many=True)
