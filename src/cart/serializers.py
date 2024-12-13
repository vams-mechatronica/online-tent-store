from rest_framework import serializers
from .models import Wishlist

# imports
from products.serializers import ProductSerialzer

class WishlistSerializer(serializers.ModelSerializer):
    item = ProductSerialzer()
    class Meta:
        model = Wishlist
        fields = '__all__'


