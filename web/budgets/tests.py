from decimal import Decimal

import pytest
from django.urls import reverse

from budgets.factories import BudgetFactory, TransactionFactory
from budgets.models import Budget
from users.factories import UserFactory


@pytest.mark.django_db
class TestBudgets:
    def setup_method(self, method):
        """ setup any state specific to the execution of the given module."""
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.budget1 = BudgetFactory(name="test1", creator=self.user1)
        self.budget2 = BudgetFactory(name="budget0", creator=self.user1)
        self.budget3 = BudgetFactory(name="third", creator=self.user2)
        self.budget4 = BudgetFactory(name="fourth", creator=self.user2, users=[self.user1])
        TransactionFactory(budget=self.budget1, amount=Decimal('30'), user=self.user1, category='test')
        TransactionFactory(budget=self.budget1, amount=Decimal('12.20'), user=self.user1)
        TransactionFactory(budget=self.budget1, amount=Decimal('-34.85'), user=self.user1)
        TransactionFactory(budget=self.budget4, user=self.user1)
        TransactionFactory(budget=self.budget4, user=self.user2)
        TransactionFactory(budget=self.budget4, user=self.user2)

    def test_transactions_sum(self):
        assert self.budget1.transactions_sum == Decimal('7.35')

    def test_budget_view_list(self, client):
        url = reverse('budgets-list')
        response = client.get(url)
        assert response.status_code == 403

        client.force_login(self.user1)
        response = client.get(url)
        assert response.status_code == 200
        assert response.json().get('count') == 3
        assert len(response.json().get('results')) == 2  # Pagination
        assert self.budget3.name not in str(response.json())

        # Filtering
        response = client.get(f'{url}?name=third')
        assert response.json().get('count') == 0  # User don't have an access to this

        response = client.get(f'{url}?transaction__category=test')
        assert len(response.json().get('results')[0].get('transaction_set')) == 1

    def test_budget_view_create(self, client):
        assert Budget.objects.count() == 4
        url = reverse('budgets-list')
        response = client.post(url, {'name': "test_name"})
        assert response.status_code == 403

        client.force_login(self.user1)
        response = client.post(url, {'name': "test_name"})
        assert response.status_code == 201
        assert Budget.objects.count() == 5
        assert Budget.objects.get(name="test_name").creator == self.user1

    def test_budget_view_update(self, client):
        budget = BudgetFactory(name="update_budget", creator=self.user1)
        url = reverse('budgets-detail', kwargs={'pk': budget.id})
        response = client.patch(url, {'users': self.user2})
        assert response.status_code == 403

        client.force_login(self.user2)
        response = client.get(url)
        assert response.status_code == 404  # No access for this budget

        client.force_login(self.user1)
        response = client.patch(url, {'users': [self.user2.id]}, content_type='application/json')
        assert response.status_code == 200
        client.force_login(self.user2)
        response = client.get(url)
        assert response.status_code == 200

    def test_budget_view_add_transaction(self, client):
        budget = BudgetFactory(name="update_budget", creator=self.user1)
        url = reverse('budgets-add-transaction', kwargs={'pk': budget.id})
        response = client.post(url, {'amount': 12.50}, content_type='application/json')
        assert response.status_code == 403

        client.force_login(self.user1)
        response = client.post(url, {'amount': 12.50}, content_type='application/json')
        print(response.json())
        assert response.status_code == 201
        assert budget.transaction_set.count() == 1
