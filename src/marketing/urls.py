from django.urls import path
from .views import *
urlpatterns = [
    path('whatsapp/inbound/webhook',whatsapp_webhook),
    path('whatsapp/send-message',send_whatsapp_message),
]
