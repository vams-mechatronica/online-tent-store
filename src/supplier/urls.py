from django.urls import path
from .views import *
urlpatterns = [
    path('detail',ServiceProviderAPI.as_view()),
    path("orders/", SupplierOrderListAPIView.as_view(), name="supplier-orders"),
    path("update-order/<int:pk>/", SupplierOrderUpdateAPIView.as_view(), name="supplier-order-update"),
    
    # SupplierTransaction APIs
    path('transactions/', SupplierTransactionListAPIView.as_view(), name='transaction-list'),
    path('transactions/create/', SupplierTransactionCreateAPIView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/', SupplierTransactionRetrieveUpdateAPIView.as_view(), name='transaction-detail-update'),

    # SupplierAccountDetails APIs
    path('accounts/create/', SupplierAccountDetailsCreateAPIView.as_view(), name='account-create'),
    path('accounts/<int:supplier__id>/', SupplierAccountDetailsRetrieveUpdateAPIView.as_view(), name='account-detail-update'),
]
