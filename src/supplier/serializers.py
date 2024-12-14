from rest_framework import serializers
from .models import SupplierOrder, ServiceProvider

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'

class SupplierOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierOrder
        fields = '__all__'
        