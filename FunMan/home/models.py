from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.utils import timezone
from .utils import time_since_post, generate_slug


User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=100)

class Comment(models.Model):
    text = models.CharField(max_length=1500)

class Post(models.Model):
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    tags = TaggableManager(blank=True)
    date = models.DateTimeField(default=timezone.now, blank=True, null=True) 
    comments = models.ManyToManyField(Comment, blank=True) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.user, self.content)
        super(Post, self).save(*args, **kwargs)
    
    def get_time_since(self):
        return time_since_post(self.date)