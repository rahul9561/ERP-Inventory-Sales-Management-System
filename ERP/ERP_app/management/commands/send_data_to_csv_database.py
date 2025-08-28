# ERP_app/management/commands/send_data_to_csv_database.py

import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from ERP_app.models import Product

class Command(BaseCommand):
    help = "Import product data from CSV into Product model"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to the CSV file (default: data/products.csv)',
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file'] or os.path.join(settings.BASE_DIR, 'data', 'products.csv')

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"❌ File not found: {file_path}"))
            return

        self.stdout.write(self.style.WARNING(f"📂 Reading data from {file_path} ..."))

        created_count = 0
        updated_count = 0

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            with transaction.atomic():
                for row in reader:
                    try:
                        product, created = Product.objects.update_or_create(
                            name=row['name'],
                            defaults={
                                "category": row.get('category', ''),
                                "price": row.get('price', 0),
                                "stock": row.get('stock', 0),
                            },
                        )
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                    except IntegrityError as e:
                        self.stderr.write(self.style.ERROR(f"⚠️ Skipped {row['name']} due to IntegrityError: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Import finished! {created_count} created, {updated_count} updated."))
