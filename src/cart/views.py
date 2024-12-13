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

# API to get wishlist for a user
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
