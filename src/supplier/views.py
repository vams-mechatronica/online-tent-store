from django.shortcuts import render
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

class SuppliersOrderAPI(generics.ListAPIView):
    serializer_class = SupplierOrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    def get_queryset(self):
        return SupplierOrder.objects.all()
    
