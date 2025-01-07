from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(WhatsappChat)
class WhatsappChatAdmin(admin.ModelAdmin):
    pass

@admin.register(WhatsappDeliveryStatus)
class WhatsappDeliveryStatusAdmin(admin.ModelAdmin):
    pass

@admin.register(WhatsAppInboundMessage)
class WhatsAppInboundMessageAdmin(admin.ModelAdmin):
    pass

@admin.register(WhatsAppOutboundMessage)
class WhatsAppOutboundMessageAdmin(admin.ModelAdmin):
    pass

@admin.register(WhatsappSeenReport)
class WhatsappSeenReportAdmin(admin.ModelAdmin):
    pass
    


    

    

    
