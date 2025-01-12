from django.urls import path
from .views import *
urlpatterns = [
    path('address',ServicableAddressAPI.as_view())
]
