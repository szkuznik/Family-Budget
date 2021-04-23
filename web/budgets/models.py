from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Budget(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_budgets')
    users = models.ManyToManyField(User, related_name='shared_budgets', verbose_name=_('Shared users'), blank=True)

    class Meta:
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')

    def __str__(self):
        return self.name

    @property
    def transactions_sum(self):
        return self.transaction_set.aggregate(Sum('amount'))['amount__sum'] or 0


class TransactionManager(models.Manager):
    def income(self):
        return self.get_queryset().filter(amount__gt=Decimal(0))

    def expenses(self):
        return self.get_queryset().filter(amount__lt=Decimal(0))


class Transaction(models.Model):
    amount = models.DecimalField(_('Amount'), decimal_places=2, max_digits=11)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    created = models.DateTimeField(_('Created at'), default=timezone.now)
    category = models.CharField(_('Category'), max_length=200, default='Uncategorized')

    objects = TransactionManager()

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return f'{self.budget.name} {self.amount}'
