from django.contrib import admin
from django.db.models import Q

from budgets.models import Budget, Transaction


class TransactionAdminInline(admin.TabularInline):
    # Todo In future we may allow user to edit his own transactions and category filtering
    fields = ['amount', 'user', 'category']
    readonly_fields = ['user']
    model = Transaction
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BudgetAdmin(admin.ModelAdmin):
    """User can edit his own budgets or see budgets to which he is added"""
    fields = ['name', 'users', 'transactions_sum']
    readonly_fields = ['transactions_sum']
    filter_horizontal = ['users']
    search_fields = ['name']
    inlines = [TransactionAdminInline]

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            obj.user = request.user
        formset.save()

    def get_queryset(self, request):
        return super().get_queryset(request).filter(Q(creator=request.user) | Q(users=request.user))

    def get_readonly_fields(self, request, obj=None):
        """We don't set has_change_permission to False because we want to allow user to add transactions"""
        if (obj and obj.creator == request.user) or (not obj):
            return self.readonly_fields
        else:
            return self.readonly_fields + ['name', 'users']


admin.site.register(Budget, BudgetAdmin)
