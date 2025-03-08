from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.utils import timezone
from .utils import time_since_post, generate_slug

User = get_user_model()

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    tags = TaggableManager(blank=True)
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    comments = models.ManyToManyField(Comment, blank=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.user, self.content)
        super(Post, self).save(*args, **kwargs)
    
    def get_time_since(self):
        return time_since_post(self.date)

    def total_likes(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists()
