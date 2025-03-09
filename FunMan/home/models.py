from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.utils import timezone
from .utils import time_since_post, generate_slug
User = get_user_model()


class Post(models.Model):
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    tags = TaggableManager(blank=True)
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)
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

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)  
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.content[:15], self.name)
    