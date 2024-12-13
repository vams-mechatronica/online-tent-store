from django.urls import path
from .views import *
urlpatterns = [
    path('create/',CreateOrderAPIView.as_view()),
    path('get/<int:pk>',RetrieveOrderAPI.as_view()),
    path('get',GetOrdersAPI.as_view()),
]
