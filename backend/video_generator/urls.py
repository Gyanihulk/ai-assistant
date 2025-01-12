from django.urls import path
from .views.video import video_list,create_video,create_video_from_images_view
from .views.image import image_list

urlpatterns = [
    path('videos/', video_list, name='video-list'),
    path('create-video/', create_video, name='create-video'),
    path('images/', image_list, name='image-list'),
    path('create-video-from-images/', create_video_from_images_view, name='create-video-from-images'),
]
