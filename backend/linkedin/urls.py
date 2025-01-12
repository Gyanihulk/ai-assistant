from django.urls import path
from .views import generate_suggestion,generate_post_comment,analyze_post

urlpatterns = [
    path('generate-suggestion/', generate_suggestion, name='generate_suggestion'),
    path('generate-post-comment/', generate_post_comment, name='generate_post_comment'),
    path('analyse-post/', analyze_post, name='analyze_post'),
]



