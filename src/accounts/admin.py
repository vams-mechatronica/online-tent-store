from django.contrib import admin
from .models import *
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display: list = ('username','first_name','mobileno','email','date_joined')
    ordering: list = ['-date_joined']
    search_fields: list = ('email','mobileno','first_name','last_name','username')

admin.site.register(CustomUser,CustomUserAdmin)

admin.site.register(UserAddresses)

@admin.register(DeviceOtp)
class DeviceOtpAdmin(admin.ModelAdmin):
    list_display = ('number','otp','status','created_date')
    search_fields = ('number',)
    ordering = ('number','otp','created_date')
    


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_code','nick_name','country_name')
    ordering = ['-country_code','-nick_name']
    search_fields = ('country_code','country_name')
    

