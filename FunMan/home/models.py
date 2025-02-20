from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ckeditor.fields import HTMLField


User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=100)

class Comment(models.Model):
    pass

class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = HTMLField()
    # categories = models.ManyToManyField(Tag) !!!!
    # tags = TaggableManager()
    date = models.DateTimeField(auto_now_add=True)
    # approved = models.BooleanField(default=True)
    comments = models.ManyToManyField(Comment, blank=True)
    # # closed = models.BooleanField(default=False)
    # # state = models.CharField(max_length=40, default="zero")

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super(Post, self).save(*args, **kwargs)

    # def __str__(self):
    #     return self.title