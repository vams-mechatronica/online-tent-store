from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(SupplierAccountDetails)
class SupplierAccountDetailsAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    pass

@admin.register(SupplierTransaction)
class SupplierTransactionAdmin(admin.ModelAdmin):
    pass

@admin.register(SupplierOrder)
class SupplierOrderAdmin(admin.ModelAdmin):
    pass

    

    


    
