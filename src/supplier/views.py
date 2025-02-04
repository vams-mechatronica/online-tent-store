from django.shortcuts import render
from rest_framework.exceptions import NotFound

from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from decimal import Decimal
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from .models import *
from .serializers import *

class ServiceProviderAPI(generics.ListCreateAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    pagination_class= PageNumberPagination
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class SupplierOrderListAPIView(generics.ListAPIView):
    serializer_class = SupplierOrderSerializer  # Create a serializer for SupplierOrder
    queryset = SupplierOrder.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        supplier_id = self.request.query_params.get("supplier_id")
        status = self.request.query_params.get("status")

        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)

        if status:
            queryset = queryset.filter(status=status)

        return queryset

class SupplierOrderUpdateAPIView(generics.UpdateAPIView):
    queryset = SupplierOrder.objects.all()
    serializer_class = SupplierOrderStatusSerializer  # Create a serializer for updating the status
    lookup_field = "pk"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
# Views for SupplierTransaction

class SupplierTransactionCreateAPIView(generics.CreateAPIView):
    queryset = SupplierTransaction.objects.all()
    serializer_class = SupplierTransactionSerializer

class SupplierTransactionListAPIView(generics.ListAPIView):
    queryset = SupplierTransaction.objects.all()
    serializer_class = SupplierTransactionSerializer

class SupplierTransactionRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = SupplierTransaction.objects.all()
    serializer_class = SupplierTransactionSerializer
    lookup_field = 'pk'

# Views for SupplierAccountDetails

class SupplierAccountDetailsCreateAPIView(generics.CreateAPIView):
    queryset = SupplierAccountDetails.objects.all()
    serializer_class = SupplierAccountDetailsSerializer

class GetSupplierAccountDetails(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        # Check if the user is a supplier
        if not self.request.user.is_supplier:
            raise NotFound("User is not a supplier")
        
        # Assuming Product model has a ForeignKey `supplier` pointing to the User model or Supplier model
        supplier = self.request.user 
        queryset = SupplierAccountDetails.objects.filter(supplier__user=supplier)
        return queryset
    serializer_class = SupplierAccountDetailsSerializer

class SupplierAccountDetailsRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = SupplierAccountDetails.objects.all()
    serializer_class = SupplierAccountDetailsSerializer
    lookup_field = 'supplier__id'  # Use supplier ID to retrieve account details
