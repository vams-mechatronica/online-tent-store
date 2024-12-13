from rest_framework import serializers
from .models import Order

# imports
from products.serializers import ProductSerialzer
from cart.serializers import WishlistSerializer


class OrderSerializer(serializers.ModelSerializer):
    items = WishlistSerializer
    class Meta:
        model = Order
        fields = '__all__'
