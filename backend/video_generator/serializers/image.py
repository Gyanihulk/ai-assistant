from rest_framework import serializers
from video_generator.models.image import  Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'prompt', 'image_url', 'created_at', 'video']
