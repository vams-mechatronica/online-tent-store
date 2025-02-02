from rest_framework import serializers
from .models import Product, ProductImage, Category,GatheringSize,PartyingForChoice,UserRequirement,PlaceChoiceForParty

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['image_url']  # Just return image URL

    def get_image_url(self, obj):
        # Return the absolute URL of the image
        return obj.image.url
class ProductSerialzer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)  

    class Meta:
        model = Product
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = '__all__'

class ImageProductSerializer(serializers.ModelSerializer):
    product = ProductSerialzer()
    class Meta:
        model = ProductImage
        fields = '__all__'

class GatheringSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatheringSize
        fields = '__all__'
    
class PartyingForChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyingForChoice
        fields = '__all__'

class UserRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequirement
        fields = '__all__'

class PlaceChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceChoiceForParty
        fields = '__all__'