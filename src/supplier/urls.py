from django.urls import path
from .views import *
urlpatterns = [
    path('detail',ServiceProviderAPI.as_view()),
    path('orders',SuppliersOrderAPI.as_view())
]
