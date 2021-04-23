import factory

from budgets.models import Budget, Transaction
from users.factories import UserFactory


class BudgetFactory(factory.django.DjangoModelFactory):
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Budget


class TransactionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    budget = factory.SubFactory(BudgetFactory)
    amount = factory.Faker('Decimal')

    class Meta:
        model = Transaction
