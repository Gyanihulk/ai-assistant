import openai
import os
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from video_generator.models.video import Video
from video_generator.serializers.video import VideoSerializer,VideoGenerationSerializer,VideoFromImagesSerializer

@api_view(['GET'])
def video_list(request):
    if request.method == 'GET':
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_video(request):
    # Use the custom VideoGenerationSerializer for handling image generation and video creation
    serializer = VideoGenerationSerializer(data=request.data)
    if serializer.is_valid():
        video = serializer.save()  # This will trigger the image generation and video creation
        print(f"{video}")
        return Response({
            'status': 'success',
            'video_file': "video.video_file"
        }, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def create_video_from_images_view(request):
    if request.method == 'POST':
        serializer = VideoFromImagesSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            return Response({
                'status': 'success',
                'video_id': video.id,
                'video_title': video.title,
                'message': 'Video created successfully from images.'
            }, status=201)
        else:
            return Response(serializer.errors, status=400)