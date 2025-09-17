from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

    def __str__(self):
        return f"{self.username} ({self.role})"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to="profileImg", blank=True, null=True)  # For base64 or URL

    def __str__(self):
        return f"{self.user.username}'s profile"


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.category})"
    
    @property
    def is_low_stock(self):
        return self.stock < 5  # threshold


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name



class Sale(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="sales")
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="sales")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Check if same sale (same product + same customer) exists
        existing_sale = Sale.objects.filter(product=self.product, customer=self.customer).first()

        if existing_sale and not self.pk:  # new entry but same product+customer found
            new_quantity = existing_sale.quantity + self.quantity

            # Prevent negative stock
            if self.product.stock < self.quantity:
                raise ValidationError("Not enough stock available.")

            # Update existing sale instead of creating new one
            existing_sale.quantity = new_quantity
            existing_sale.total_price = self.product.price * new_quantity

            # Reduce stock
            self.product.stock -= self.quantity
            if self.product.stock < 0:
                raise ValidationError("Stock cannot go negative.")
            self.product.save()

            existing_sale.save()
            return existing_sale  # return updated sale instead of creating a new one

        # If total_price not set manually, auto calculate
        if not self.total_price:
            self.total_price = self.product.price * self.quantity

        # On new sale (unique product-customer), reduce stock
        if not self.pk:
            if self.product.stock < self.quantity:
                raise ValidationError("Not enough stock available.")
            self.product.stock -= self.quantity
            self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale of {self.product.name} ({self.quantity}) - {self.total_price}"



from django.db.models import Sum

class Chart(models.Model):
    CHART_TYPE_CHOICES = (
        ("total_sales", "Total Sales"),
        ("total_stock", "Total Stock"),
        ("total_customers", "Total Customers"),
    )

    title = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    chart_type = models.CharField(max_length=20, choices=CHART_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_value(self):
        """Calculate value based on chart_type without saving"""
        if self.chart_type == "total_sales":
            total = Sale.objects.aggregate(total=Sum("total_price"))["total"] or 0
            self.value = total

        elif self.chart_type == "total_stock":
            total = Product.objects.aggregate(total=Sum("stock"))["total"] or 0
            self.value = total

        elif self.chart_type == "total_customers":
            self.value = Customer.objects.count()

    def save(self, *args, **kwargs):
        # Update value before saving
        self.update_value()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.chart_type})"




from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class Invoice(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_address = models.TextField()
    invoice_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    # 👇 This is only for type checking, won't affect database
    items: "RelatedManager[InvoiceItem]"
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def line_total(self):
        return (self.quantity * self.price) + self.tax
