from rest_framework import serializers
from .models import SupplierOrder, ServiceProvider,SupplierTransaction,SupplierAccountDetails

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'

class SupplierOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierOrder
        fields = '__all__'

class SupplierOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierOrder
        fields = ["status"]


class SupplierTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierTransaction
        fields = '__all__'

class SupplierAccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierAccountDetails
        fields = '__all__'