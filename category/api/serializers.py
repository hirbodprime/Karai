from rest_framework import serializers
from django.conf import settings
from category.models import (CategoryModel,)

class BaseCategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    image = serializers.ImageField(read_only=True)

    class Meta:
        abstract = True
        fields = ['hidden','id', 'name', 'slug', 'description', 'created_at', 'updated_at']


class CategorySerializer(BaseCategorySerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        # Get the current request object
        request = self.context.get('request')

        # Check if the object has a 'photo' field
        if obj.image:
            # Get the full URL for the photo by prepending the domain
            return f"{settings.SITE_DOMAIN}{obj.image.url}"
        else:
            return None

    class Meta:
        model = CategoryModel
        fields = ['id', 'name', 'slug', 'description', 'image', 'created_at', 'updated_at']
