from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/video/', include('video_generator.urls')),  # Video Generator APIs
    path('api/linkedin/', include('linkedin.urls')),      # LinkedIn APIs
]
