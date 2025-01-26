from django.contrib import admin
from django.urls import path,include, re_path, register_converter
from .utils import HashIdConverter, FloatConverter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

...

schema_view = get_schema_view(
   openapi.Info(
      title="Online APIs",
      default_version='v1',
      description="API service for multiple applications",
      terms_of_service="https://www.vamsbookstore.in/terms-of-service/",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


admin.site.site_header = "Admin"
admin.site.index_title = "Admin"
admin.site.site_title = "Admin"

register_converter(HashIdConverter, "hashid")
register_converter(FloatConverter, "float")

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0)),
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
