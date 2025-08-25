# ERP/ERP_app/views.py
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .models import Product, Customer, Sale
from .serializers import ProductSerializer, CustomerSerializer, SaleSerializer,RegisterSerializer, UserSerializer
# Create your views here.




User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-date')
    serializer_class = SaleSerializer
