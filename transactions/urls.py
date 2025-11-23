from .views import TransactionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
