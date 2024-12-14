from django.shortcuts import render
import razorpay
from django.conf import settings
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
from datetime import datetime,timezone

from orders.models import Order


# Initialize Razorpay client
razorpay_api = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_KEY_SECRET)
)

class CreatePaymentAPI(APIView):
    def get(self, request, order_id):
        try:
            # Fetch the order by ID
            order = Order.objects.get(pk=order_id)

            # Determine the amount based on payment type
            payment_type = request.query_params.get('payment_type', None)
            if payment_type not in ['advance', 'full']:
                return Response({"error": "Invalid payment_type. Use 'advance' or 'full'."}, status=status.HTTP_400_BAD_REQUEST)

            amount = order.booking_amount if payment_type == 'advance' else order.total_amount

            # Convert amount to paise (Razorpay accepts amounts in paise)
            amount_in_paise = int(amount * 100)

            # Create Razorpay order
            razorpay_order = razorpay_api.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": 1  # Auto capture payment
            })

            # Update the order with Razorpay order ID
            payment_details, _ = Payment.objects.get_or_create(order=order)
            if payment_type == 'advance':
                is_booking_amount = True
                payment_details.advance_amount = amount
                payment_details.advance_date = datetime.now()
                payment_details.advance_payment_id = razorpay_order['id']
                # payment_details.advance_payment_transaction_id = razorpay_order.get('transaction_id')
            elif payment_type == 'full':
                is_booking_amount = False
                payment_details.pending_amount = amount
                payment_details.pending_date = datetime.now()
                payment_details.pending_payment_id = razorpay_order['id']
                # payment_details.pending_payment_transaction_id = razorpay_order.get('transaction_id')
            
            payment_details.save()


            return Response({
                "order_id":order_id,
                "razorpay_order_id": razorpay_order['id'],
                "amount": amount,
                "currency": "INR",
                "payment_type": payment_type,
                "is_booking_payment":is_booking_amount
            }, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyPaymentAPI(APIView):
    def post(self, request):
        try:
            # Extract data from the request
            razorpay_order_id = request.data.get('razorpay_order_id')
            razorpay_payment_id = request.data.get('razorpay_payment_id')
            razorpay_signature = request.data.get('razorpay_signature')

            if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                return Response({"error": "Missing payment details."}, status=status.HTTP_400_BAD_REQUEST)

            # Verify the payment signature
            params = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            razorpay_api.utility.verify_payment_signature(params)

            # Update order status
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.payment_status = 'paid'
            order.razorpay_payment_id = razorpay_payment_id
            order.save()

            return Response({"message": "Payment verified and order updated successfully."}, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "Invalid payment signature."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentSuccessUpdateAPI(APIView):
    def get(self, request):
        # def razorpay_success_redirect(request):
        razorpay_order_id = request.GET.get("razorpay_order_id")
        razorpay_payment_id = request.GET.get("razorpay_payment_id")
        order_id = request.GET.get('order_id')
        is_partial = request.GET.get('is_booking_amount')
        # selected_billing_address = BillingAddress.objects.get(user=request.user, is_default=True)
        if request.user and order_id:
            order = Order.objects.get(user=request.user, payment_status=False,pk=order_id)
            payment_detail = Payment.objects.get(order=order)
            if is_partial:
                payment_detail.advance_payment_transaction_id = razorpay_payment_id
                order.is_partial_payment_paid = True
            else:
                payment_detail.pending_payment_transaction_id = razorpay_payment_id
                order.is_full_payment_paid = True
            payment_detail.save()
            order.save()
        return Response({'message':
                         'Payment Successful'},status=status.HTTP_200_OK)


