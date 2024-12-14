from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','size','unit_base_price')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

@admin.register(GatheringSize)
class GatheringSizeAdmin(admin.ModelAdmin):
    pass

@admin.register(PartyingForChoice)
class PartyingForChoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(UserRequirement)
class UserRequirementAdmin(admin.ModelAdmin):
    pass
    

    

    

    

    

    
