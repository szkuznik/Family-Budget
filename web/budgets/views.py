from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from budgets.models import Budget
from budgets.serializers import BudgetSerializer, TransactionSerializer
from familybudget.permissions import IsCreatorOrReadOnly


class BudgetViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'transaction__category', 'transaction__user']

    def get_queryset(self):
        return Budget.objects.filter(Q(creator=self.request.user) | Q(users=self.request.user))

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(methods=['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def add_transaction(self, request, pk):
        instance = self.get_object()
        serializer = TransactionSerializer(data=request.data | {'budget': instance.id, 'user': request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
