from django.urls import path
from .views import *
urlpatterns = [
    path('whatsapp/inbound/webhook',whatsapp_webhook),
    path('whatsapp/send-message',send_whatsapp_message),
    path('whatsapp/delivery-status/add',add_delivery_status),
    path('whatsapp/delivery-status/get',get_delivery_status),
    path('whatsapp/seen-report/add',add_seen_report)

]
