import datetime

from django.core.exceptions import ValidationError
from rest_framework import serializers

from app.transaction.models import Transaction, TransactionLineItem


def validate_date_range(self, date_start, date_end):
    date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d').date()
    date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()

    if date_start > date_end:
        raise ValidationError("date_start cannot be more recent than date_end")


class TransactionLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLineItem
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    transaction_line_items = TransactionLineItemSerializer(allow_null=False, required=True, many=True)

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionLineItemCreateSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(required=True, source='debtor')
    paid = serializers.DecimalField(max_digits=100, decimal_places=2)
    owes = serializers.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        model = TransactionLineItem
        fields = [
            'owes',
            'paid',
            'user',
        ]


class TransactionCreateSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(required=True, max_length=3, min_length=3)
    total = serializers.DecimalField(required=True, decimal_places=2, max_digits=100)
    user_shares = TransactionLineItemCreateSerializer(allow_null=False, required=True, many=True)
    split_type = serializers.ChoiceField(choices=['percent', 'money'])

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


class TransactionIdSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Transaction.objects.all())

    class Meta:
        model = Transaction
        fields = ['id']


class TransactionLineItemUpdateSerializer(serializers.ModelSerializer):
    transaction_line_item = serializers.IntegerField(required=True, source='id')

    class Meta:
        model = TransactionLineItem
        fields = ['transaction_line_item', 'resolved']


class TransactionUpdateSerializer(serializers.ModelSerializer):
    transaction = serializers.IntegerField(required=True, source='id')
    transaction_line_items = TransactionLineItemUpdateSerializer(allow_null=False, required=True, many=True)

    class Meta:
        model = Transaction
        fields = ['transaction', 'transaction_line_items']
