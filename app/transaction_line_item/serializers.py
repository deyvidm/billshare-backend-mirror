from rest_framework import serializers

from app.transaction.models import Transaction
from app.transaction_line_item.models import TransactionLineItem


class TransactionLineItemOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLineItem
        fields = ['payer', 'owes', 'paid']

    paid = serializers.DecimalField(max_digits=100, decimal_places=2)
    owes = serializers.DecimalField(max_digits=100, decimal_places=2)


class TransactionIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id']


class UpdateTransactionLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLineItem
        fields = ['id', 'resolved']
