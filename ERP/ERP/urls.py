
from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from ERP_app.views import RegisterView, UserListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ERP_app.urls')),
    # JWT authentication endpoints
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/", UserListView.as_view(), name="user_list"),
    path("api/auth/verify/", TokenVerifyView.as_view(), name="token_verify"),

]







  