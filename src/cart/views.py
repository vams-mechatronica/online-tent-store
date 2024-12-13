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

# imports
from accounts.models import CustomUser
from products.models import Product
import razorpay

razorpay_api = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_KEY_SECRET)
)

class WishlistAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        ordered = request.query_params.get('ordered', 'false').lower() == 'true'

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Filter products based on user_id and ordered status
            wishlist_items = Wishlist.objects.filter(user_id=user_id, ordered=ordered)

            # Serialize the wishlist items
            wishlist_serializer = WishlistSerializer(wishlist_items, many=True)

            return Response(wishlist_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WishlistPostAPI(APIView):
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            item_id = request.data.get("item_id")
            quantity = request.data.get("quantity", 1)

            if not user_id or not item_id:
                return Response(
                    {"error": "Both user_id and item_id are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validate user and item
            try:
                user = CustomUser.objects.get(pk=user_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                item = Product.objects.get(pk=item_id)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if the item is already in the user's wishlist
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                item=item,
                defaults={"quantity": quantity},
            )

            if not created:
                wishlist_item.quantity += quantity
                wishlist_item.save()

            wishlist_serializer = WishlistSerializer(wishlist_item)

            return Response(
                wishlist_serializer.data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


