from django.urls import path
from .views import *
urlpatterns = [
    path('get-items',WishlistAPIView.as_view()),
    path('add-items',WishlistPostAPI.as_view())
]
