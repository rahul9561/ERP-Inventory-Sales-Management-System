# ERP/ERP_app/views.py
from rest_framework import generics, permissions ,response , status
from rest_framework.views import APIView
from rest_framework.decorators import action
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
    



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer




from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import tempfile, os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @action(detail=True, methods=['get'])
    def generate_pdf(self, request, pk=None):
        invoice = self.get_object()

        # Make sure items exist
        items = getattr(invoice, "items", None)
        if not items:
            return Response({"error": "No items found for invoice"}, status=400)

        # Create temporary PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            pdf_path = tmpfile.name

        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30*mm, height - 30*mm, f"Invoice #{invoice.id}")

        # Customer info
        c.setFont("Helvetica", 12)
        c.drawString(30*mm, height - 40*mm, f"Customer: {getattr(invoice, 'customer_name', 'N/A')}")
        c.drawString(30*mm, height - 50*mm, f"Date: {getattr(invoice, 'date', '')}")

        # Table header
        c.setFont("Helvetica-Bold", 12)
        y = height - 70*mm
        c.drawString(30*mm, y, "Item")
        c.drawString(100*mm, y, "Qty")
        c.drawString(120*mm, y, "Price")
        c.drawString(150*mm, y, "Total")

        # Table rows
        c.setFont("Helvetica", 11)
        y -= 10*mm
        total = 0
        for item in invoice.items.all():
            line_total = item.quantity * item.price
            total += line_total
            c.drawString(30*mm, y, str(item.product))
            c.drawString(100*mm, y, str(item.quantity))
            c.drawString(120*mm, y, f"{item.price:.2f}")
            c.drawString(150*mm, y, f"{line_total:.2f}")
            y -= 10*mm

        # Grand total
        c.setFont("Helvetica-Bold", 12)
        c.drawString(120*mm, y - 10*mm, "Total:")
        c.drawString(150*mm, y - 10*mm, f"{total:.2f}")

        c.showPage()
        c.save()

        return FileResponse(
            open(pdf_path, "rb"),
            content_type="application/pdf",
            as_attachment=True,
            filename=f"invoice_{pk}.pdf"
        )
