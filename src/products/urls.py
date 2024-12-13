from django.urls import path
from .views import *
urlpatterns = [
    path('all',ProductAPI.as_view()),
    path('images',ProductImageAPI.as_view()),
    path('category',CategoryAPI.as_view()),
    path('product-category',ProductCategoryAPI.as_view()),
    path('product-images/<int:pk>',ProductImagesAPIView.as_view()),
]
