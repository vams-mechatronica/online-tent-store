from rest_framework import serializers
from .models import ServicableAddress

class ServicableAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicableAddress
        fields = '__all__'
