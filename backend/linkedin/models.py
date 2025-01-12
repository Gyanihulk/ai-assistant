from django.db import models

class Post(models.Model):
    content = models.TextField()
    category = models.CharField(max_length=255, null=True, blank=True)
    generated_comment = models.TextField(null=True, blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post ID: {self.id}, Category: {self.category}"

class AnalyzedPost(models.Model):
    post_id = models.CharField(max_length=255, unique=True)
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)
    content = models.TextField()
    reactions = models.JSONField(default=dict, blank=True)
    media_url = models.URLField(blank=True, null=True)
    comments = models.JSONField(default=list, blank=True)
    categories = models.JSONField(default=list, blank=True)
    analysis = models.JSONField(default=dict, blank=True)
    generated_comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_id
    