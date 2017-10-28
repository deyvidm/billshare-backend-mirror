from rest_framework import serializers

from app.transaction.models import Transaction
from app.transaction_line_item.serializers import TransactionLineItemOperationSerializer


class TransactionOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['label', 'group', 'creator', 'total', 'currency_code', 'transaction_line_items']

    total = serializers.DecimalField(required=True, decimal_places=2, max_digits=100)
    currency_code = serializers.CharField(required=True, max_length=3, min_length=3)
    transaction_line_items = TransactionLineItemOperationSerializer(many=True)
