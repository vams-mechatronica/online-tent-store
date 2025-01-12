from django.contrib import admin
from .models import ServicableAddress


# Register your models here.
@admin.register(ServicableAddress)
class ServicableAddressAdmin(admin.ModelAdmin):
    list_display = ('area','city','state','pincode')
    search_fields = ('area','city','state','pincode')
    ordering = ('area','city','state','pincode')
    
