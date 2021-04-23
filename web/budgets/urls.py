from rest_framework import routers

from budgets.views import BudgetViewSet

router = routers.SimpleRouter()
router.register('budgets', BudgetViewSet, basename='budgets')
urlpatterns = router.urls
