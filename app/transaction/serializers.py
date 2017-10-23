from rest_framework import serializers

from app.transaction.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['payer', 'owes', 'paid']

    paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    owes = serializers.DecimalField(max_digits=10, decimal_places=2)


class TransactionIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id']


class UpdateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'resolved']
