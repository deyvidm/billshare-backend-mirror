from rest_framework import serializers

from app.transaction.models import Transaction, TransactionLineItem


class TransactionLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLineItem
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    transaction_line_items = TransactionLineItemSerializer(allow_null=False, required=True, many=True)


class TransactionLineItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLineItem
        fields = [
            'owes',
            'paid',
            'user',
        ]

    user = serializers.IntegerField(required=True, source='debtor')
    paid = serializers.DecimalField(max_digits=100, decimal_places=2)
    owes = serializers.DecimalField(max_digits=100, decimal_places=2)


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'creator',
            'currency_code',
            'group',
            'label',
            'total',
            'user_shares',
            'split_type'
        ]
    currency_code = serializers.CharField(required=True, max_length=3, min_length=3)
    total = serializers.DecimalField(required=True, decimal_places=2, max_digits=100)
    user_shares = TransactionLineItemCreateSerializer(allow_null=False, required=True, many=True)
    split_type = serializers.ChoiceField(choices=["percent", "money"])


class TransactionIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id']


class TransactionLineItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLineItem
        fields = ['transaction_line_item', 'resolved']

    transaction_line_item = serializers.IntegerField(required=True, source='id')


class TransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction', 'transaction_line_items']

    transaction = serializers.IntegerField(required=True, source='id')
    transaction_line_items = TransactionLineItemUpdateSerializer(allow_null=False, required=True, many=True)
