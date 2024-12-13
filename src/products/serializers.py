from rest_framework import serializers
from .models import Product, ProductImage, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = '__all__'

class ImageProductSerializer(serializers.ModelSerializer):
    product = ProductSerialzer()
    class Meta:
        model = ProductImage
        fields = '__all__'