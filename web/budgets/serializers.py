from rest_framework import serializers

from budgets.models import Budget, Transaction


class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        for field, value in self.context['request'].GET.items():
            splitted = field.split('transaction__')
            if len(splitted) == 2 and field in self.context['view'].filterset_fields:
                data = data.filter(**{splitted[1]: value})
        return super(FilteredListSerializer, self).to_representation(data)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        list_serializer_class = FilteredListSerializer


class BudgetSerializer(serializers.ModelSerializer):
    transaction_set = TransactionSerializer(many=True, read_only=True)
    creator = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Budget
        fields = ['id', 'name', 'creator', 'users', 'transactions_sum', 'transaction_set']
