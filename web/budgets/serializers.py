from rest_framework import serializers

from budgets.models import Budget, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class BudgetSerializer(serializers.ModelSerializer):
    transaction_set = TransactionSerializer(many=True, read_only=True)
    creator = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Budget
        fields = ['id', 'name', 'creator', 'users', 'transactions_sum', 'transaction_set']
