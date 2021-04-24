import factory

from budgets.models import Budget, Transaction
from users.factories import UserFactory


class BudgetFactory(factory.django.DjangoModelFactory):
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Budget

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of users were passed in, use them
            for user in extracted:
                self.users.add(user)


class TransactionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    budget = factory.SubFactory(BudgetFactory)
    amount = factory.Faker('pyint')

    class Meta:
        model = Transaction
