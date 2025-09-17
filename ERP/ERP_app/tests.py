from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import User, Product, Customer, Sale, Chart, Invoice, InvoiceItem
from decimal import Decimal
from datetime import date, timedelta


class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(name="Laptop", category="Electronics", price=1000, stock=10)
        self.assertEqual(product.name, "Laptop")
        self.assertFalse(product.is_low_stock)


class SaleModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Phone", category="Electronics", price=500, stock=10)
        self.customer = Customer.objects.create(name="Rahul", email="rahul@example.com", phone="9999999999")

    def test_sale_reduces_stock(self):
        sale = Sale.objects.create(product=self.product, customer=self.customer, quantity=2)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)
        self.assertEqual(sale.total_price, Decimal("1000"))

    def test_sale_not_enough_stock(self):
        with self.assertRaises(ValidationError):
            Sale.objects.create(product=self.product, customer=self.customer, quantity=20)


class ChartModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Tablet", category="Electronics", price=300, stock=5)
        self.customer = Customer.objects.create(name="John", email="john@example.com", phone="8888888888")
        Sale.objects.create(product=self.product, customer=self.customer, quantity=2)

    def test_total_sales_chart(self):
        chart = Chart.objects.create(title="Sales Chart", chart_type="total_sales")
        self.assertGreater(chart.value, 0)

    def test_total_stock_chart(self):
        chart = Chart.objects.create(title="Stock Chart", chart_type="total_stock")
        self.assertGreaterEqual(chart.value, 0)

    def test_total_customers_chart(self):
        chart = Chart.objects.create(title="Customers Chart", chart_type="total_customers")
        self.assertEqual(chart.value, 1)


class InvoiceModelTest(TestCase):
    def test_invoice_total(self):
        invoice = Invoice.objects.create(
            customer_name="Rahul Kumar",
            customer_email="rahul@example.com",
            customer_address="123 Street",
            due_date=date.today() + timedelta(days=7),
        )
        InvoiceItem.objects.create(invoice=invoice, product="Chair", quantity=2, price=100, tax=10)
        InvoiceItem.objects.create(invoice=invoice, product="Table", quantity=1, price=200, tax=20)

        items = invoice.items.all()
        total = sum(item.line_total for item in items)
        invoice.total = total
        invoice.save()

        self.assertEqual(invoice.total, Decimal("430.00"))
