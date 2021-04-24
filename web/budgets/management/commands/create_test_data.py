from decimal import Decimal

from django.core.management import BaseCommand

from budgets.factories import BudgetFactory, TransactionFactory
from users.factories import UserFactory


class Command(BaseCommand):
    help = 'Create initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--superuser',
            action='store_true',
            help='Create superuser admin with password admin1234',
        )

    def handle(self, *args, **options):
        user1 = UserFactory()
        user2 = UserFactory()
        budget1 = BudgetFactory(name="test1", creator=user1)
        budget2 = BudgetFactory(name="budget0", creator=user1)
        budget3 = BudgetFactory(name="third", creator=user2)
        budget4 = BudgetFactory(name="fourth", creator=user2, users=[user1])
        TransactionFactory(budget=budget1, amount=Decimal('30'), user=user1, category='test')
        TransactionFactory(budget=budget1, amount=Decimal('12.20'), user=user1)
        TransactionFactory(budget=budget1, amount=Decimal('-34.85'), user=user1)
        TransactionFactory(budget=budget4, user=user1)
        TransactionFactory(budget=budget4, user=user2)
        TransactionFactory(budget=budget4, user=user2)

        if options['superuser']:
            user1.is_superuser = True
            user1.username = 'admin'
            user1.set_password('admin1234')
            user1.save()

        self.stdout.write(self.style.SUCCESS('Successfully created objects'))
