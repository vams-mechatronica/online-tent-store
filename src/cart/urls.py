from django.urls import path
from .views import *
urlpatterns = [
    path('get-items',WishlistAPIView.as_view())
]
