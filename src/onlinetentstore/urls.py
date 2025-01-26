from django.contrib import admin
from django.urls import path,include, re_path, register_converter
from .utils import HashIdConverter, FloatConverter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

...
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # Schema endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Other endpoints
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('accounts.urls')),
    path('api/v1/product/', include('products.urls')),
    path('api/v1/wishlist/', include('cart.urls')),
    path('api/v1/order/', include('orders.urls')),
    path('api/v1/payment/', include('payments.urls')),
    path('api/v1/supplier/', include('supplier.urls')),
    path('api/v1/marketing/', include('marketing.urls')),
    path('api/v1/service/',include('service.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
