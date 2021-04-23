from decimal import Decimal

import pytest

from budgets.factories import BudgetFactory, TransactionFactory


@pytest.mark.django_db
def test_transactions_sum():
    budget = BudgetFactory()
    TransactionFactory(budget=budget, amount=Decimal('30'))
    TransactionFactory(budget=budget, amount=Decimal('12.20'))
    TransactionFactory(budget=budget, amount=Decimal('-34.85'))
    assert budget.transactions_sum == Decimal('7.35')



