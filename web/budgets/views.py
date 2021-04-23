# from django.db.models import Q
# from django.shortcuts import render
# from rest_framework import viewsets
#
# from budgets.models import Budget
#
#
# class BudgetViewSet(viewsets.ModelViewSet):
#     def get_queryset(self):
#         return Budget.objects.filter(Q(creator=self.request.user) | Q(users=self.request.user))
