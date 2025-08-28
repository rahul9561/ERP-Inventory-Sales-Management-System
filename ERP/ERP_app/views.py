# ERP/ERP_app/views.py
from rest_framework import generics, permissions ,response , status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .models import *
from .serializers import *
from .permissions import IsAdmin, IsManager, IsStaff
# Create your views here.




User = get_user_model()

class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-date')
    serializer_class = SaleSerializer




from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum

@api_view(["GET"])
def dashboard(request):
    data = {
        "total_sales": Sale.objects.aggregate(Sum("total_price"))["total_price__sum"] or 0,
        "total_stock": Product.objects.aggregate(Sum("stock"))["stock__sum"] or 0,
        "total_customers": Customer.objects.count(),
    }
    return Response(data)





class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

    # Optional: Update chart values on GET
    def get_queryset(self):
        queryset = super().get_queryset()
        for chart in queryset:
            chart.update_value()
        return queryset
    


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by("-created_at")
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated & (IsAdmin | IsManager)]  # Only Admin/Manager

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
