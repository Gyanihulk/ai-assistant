from django.urls import path
from .views import generate_suggestion,generate_post_comment,analyze_post,generate_suggested_reply

urlpatterns = [
    path('generate-suggestion/', generate_suggestion, name='generate_suggestion'),
    path('generate-post-comment/', generate_post_comment, name='generate_post_comment'),
    path('generate-message-suggestion/', generate_suggested_reply, name='generate_suggested_reply'),
    path('analyse-post/', analyze_post, name='analyze_post'),
]






