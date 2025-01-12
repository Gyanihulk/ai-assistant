from django.db import models

class Image(models.Model):
    prompt = models.TextField()
    image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='image_videos', null=True, blank=True)

    def __str__(self):
        return f"Image for video: {self.video.title} - Prompt: {self.prompt}"
