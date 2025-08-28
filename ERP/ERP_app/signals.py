from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Sale)
@receiver(post_save, sender=Product)
@receiver(post_save, sender=Customer)
def update_charts(sender, instance, **kwargs):
    for chart in Chart.objects.all():
        chart.update_value()
        chart.save()




from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=InvoiceItem)
def update_stock_and_total(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock -= instance.quantity
        product.save()

        # Update Invoice total
        invoice = instance.invoice
        total = sum(item.line_total() for item in invoice.items.all())
        invoice.total_amount = total
        invoice.save()

