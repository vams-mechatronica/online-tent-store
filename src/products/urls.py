from django.urls import path
from .views import *
urlpatterns = [
    path('all',ProductAPI.as_view()),
    path('images',ProductImageAPI.as_view()),
    path('create',ProductPostAPI.as_view()),
    path('images/create',ProductImagePostAPI.as_view()),
    path('category',CategoryAPI.as_view()),
    path('product-category',ProductCategoryAPI.as_view()),
    path('product-images/<int:pk>',ProductImagesAPIView.as_view()),
    path('gathering-size',GetheringSizeAPI.as_view()),
    path('party-choices',PartyingForChoiceAPI.as_view()),
    path('get-estimate',UserRequirementAPI.as_view()),
    path('place-type',PlaceTypeAPI.as_view()),
]
