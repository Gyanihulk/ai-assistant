from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    length_seconds = models.IntegerField()
    topic = models.CharField(max_length=255)
    orientation = models.CharField(max_length=50)
    published_at = models.DateTimeField(null=True, blank=True)
    images = models.ManyToManyField('Image', related_name='videos')
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.title
