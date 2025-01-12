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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import *
from .serializers import *


class ServicableAddressAPI(generics.ListCreateAPIView):
    queryset = ServicableAddress.objects.all()
    serializer_class = ServicableAddressSerializer
    pagination_class= PageNumberPagination
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)
    filterset_fields = ['area','city','state','pincode']
    search_fields = ['area','city','state','pincode']