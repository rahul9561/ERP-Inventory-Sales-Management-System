from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'charts', ChartViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # dashboard
    path("dashboard/", dashboard, name="dashboard"),
    # auth
    path("auth/current/", CurrentUserView.as_view(), name="current_user"),
    path("users/", UserListView.as_view(), name="user_list"),
]   
