from django.urls import path
from .views import *
urlpatterns = [
    path('create/<int:order_id>',CreatePaymentAPI.as_view()),
    path('verify',VerifyPaymentAPI.as_view()),
    path('success',PaymentSuccessUpdateAPI.as_view()),
]
