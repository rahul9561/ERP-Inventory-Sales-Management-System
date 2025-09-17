from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_img = serializers.ImageField(
        source='profile.profile_img',
        allow_null=True,
        required=False
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role", "profile_img"]

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", {})
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data.get("role", "staff"),
            # profile_img=validated_data["profile_img"],
        )
        user.set_password(validated_data["password"])
        user.save()

        if profile_data:
            user.profile.profile_img = profile_data.get("profile_img")
            user.profile.save()

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.role = validated_data.get("role", instance.role)

        if "password" in validated_data:
            instance.set_password(validated_data["password"])

        instance.save()

        if profile_data:
            instance.profile.profile_img = profile_data.get(
                "profile_img", instance.profile.profile_img
            )
            instance.profile.save()

        return instance



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data.get("role", "staff"),  # default role if not provided
        )
        user.set_password(validated_data["password"])  # hash the password
        user.save()
        return user

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data.get("role", "staff"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class SaleSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    customer_name = serializers.CharField(source="customer.name", read_only=True)

    class Meta:
        model = Sale
        fields = "__all__"


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = "__all__"




# Serializers
# Serializers
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone']

class ProductSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'stock', 'is_low_stock']

class InvoiceItemSerializer(serializers.ModelSerializer):
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceItem
        fields = ['id', 'product', 'quantity', 'price', 'tax', 'line_total']

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = Invoice
        fields = ['id', 'customer_name', 'customer_email', 'customer_address', 
                 'invoice_date', 'due_date', 'status', 'total', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        invoice.total = sum(item.line_total for item in invoice.items.all())
        invoice.save()
        return invoice

    def update(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = self.instance
        for attr, value in validated_data.items():
            setattr(invoice, attr, value)
        invoice.save()
        
        # Update or create items
        existing_item_ids = set(invoice.items.values_list('id', flat=True))
        submitted_item_ids = set(item.get('id', None) for item in items_data if item.get('id'))
        
        # Delete items not in the update
        invoice.items.exclude(id__in=submitted_item_ids).delete()
        
        # Update or create items
        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id:
                item = invoice.items.get(id=item_id)
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
            else:
                InvoiceItem.objects.create(invoice=invoice, **item_data)
                
        invoice.total = sum(item.line_total for item in invoice.items.all())
        invoice.save()
        return invoice