"""
URL configuration for onlinetentstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path, register_converter
from .utils import HashIdConverter, FloatConverter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Online Tent Booking",
      default_version='v1',
      description="Book Tents for Your Celebrations online",
      terms_of_service="https://www.vamscentral.com/about/terms-of-service",
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
    path('account/',include('accounts.urls')),
    path('product/',include('products.urls')),
    path('wishlist/',include('cart.urls')),
    path('order/',include('orders.urls')),
    path('payment/',include('payments.urls')),
]
