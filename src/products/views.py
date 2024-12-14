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
# Create your views here.
class ProductAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialzer
    pagination_class = PageNumberPagination

class ProductPostAPI(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialzer
    pagination_class = PageNumberPagination
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)

class ProductImageAPI(generics.ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    pagination_class = PageNumberPagination

class ProductImagePostAPI(generics.CreateAPIView):
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    pagination_class = PageNumberPagination

class CategoryAPI(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

class ProductCategoryAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCategorySerializer
    pagination_class = PageNumberPagination

class GetheringSizeAPI(generics.ListAPIView):
    queryset = GatheringSize.objects.all()
    serializer_class = GatheringSizeSerializer
    pagination_class = PageNumberPagination

class PartyingForChoiceAPI(generics.ListAPIView):
    queryset = PartyingForChoice.objects.all()
    serializer_class = PartyingForChoiceSerializer
    pagination_class = PageNumberPagination

class UserRequirementAPI(generics.ListCreateAPIView):
    serializer_class = UserRequirementSerializer
    pagination_class = PageNumberPagination
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        return UserRequirement.objects.get(user=self.request.user)

class ProductImagesAPIView(APIView):
    def get(self, request, pk):
        try:
            # Fetch the product by primary key (pk)
            product = Product.objects.get(pk=pk)

            # Serialize product data
            product_serializer = ProductSerialzer(product)

            # Fetch all related images for the product
            images = ProductImage.objects.filter(product=product)

            # Serialize image data
            image_serializer = ProductImageSerializer(images, many=True)

            # Prepare the response data
            response_data = {
                'name': product_serializer.data['name'],
                'images': [image['image'] for image in image_serializer.data]
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)