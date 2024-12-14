from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from cart.models import Wishlist
from .models import Order
from .serializers import OrderSerializer
from coupon.models import Coupon
from payments.models import Payment  # Assuming a Payment model exists
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication


class CreateOrderAPIView(APIView):
    authentication_classes = (BasicAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        coupon_code = request.data.get("coupon_code")
        # payment_data = request.data.get("payment_data")

        try:
            # # Validate payment data
            # if payment_data and not {"amount", "payment_id", "transaction_id"} <= payment_data.keys():
            #     return Response({"error": "Invalid payment data."}, status=status.HTTP_400_BAD_REQUEST)

            # Create order and optionally handle payment
            with transaction.atomic():
                # Fetch wishlist items
                wishlist_items = Wishlist.objects.filter(user=user, ordered=False)
                if not wishlist_items.exists():
                    return Response({"error": "No items in the wishlist to create an order."}, status=status.HTTP_400_BAD_REQUEST)

                # Calculate total amount
                total_amount = sum(item.item.unit_base_price * item.quantity for item in wishlist_items if item.item)

                # Apply coupon if provided
                coupon = None
                final_amount = total_amount
                if coupon_code:
                    try:
                        coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                        discount = coupon.get_discount_amount(total_amount)
                        final_amount = total_amount - discount
                    except Coupon.DoesNotExist:
                        return Response({"error": "Invalid or inactive coupon code."}, status=status.HTTP_400_BAD_REQUEST)

                # Create the order
                order = Order.objects.create(
                    user=user,
                    items=[
                        {
                            "item_id": item.item.id,
                            "name": item.item.name,
                            "price": item.item.unit_base_price,
                            "quantity": item.quantity,
                        }
                        for item in wishlist_items
                    ],
                    total_amount=total_amount,
                    coupon=coupon,
                    final_amount=final_amount,
                )

                # Mark wishlist items as ordered
                # wishlist_items.update(ordered=True)

            return Response({"message": "Order created successfully.", "order_id": order.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetOrdersAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Fetch orders for the authenticated user
        return Order.objects.filter(user=self.request.user)

class RetrieveOrderAPI(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk" 

    def get_queryset(self):
        # Ensure only the authenticated user's orders can be accessed
        return Order.objects.filter(user=self.request.user)


