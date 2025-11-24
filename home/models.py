from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.utils import timezone
from .services import time_since_post, generate_slug
import uuid
import os

User = get_user_model()

def get_media_upload_path(instance, filename):
    # генерация пути для загрузки медиа файлов
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f"posts/{instance.post.user.id}/{filename}"


class Post(models.Model):
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, default="")
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
    
    def get_media(self):
        return self.media.all()
    
    def has_media(self):
        return self.media.exists()

class MediaFile(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_media_upload_path)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['uploaded_at']
    
    def save(self, *args, **kwargs):
        #тип файла по расширению
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                self.media_type = 'image'
            elif ext in ['.mp4', '.mov', '.webm']:
                self.media_type = 'video'
            
            # размер файла
            if hasattr(self.file, 'size'):
                self.file_size = self.file.size
        
        super().save(*args, **kwargs)
    
    @property
    def is_image(self):
        return self.media_type == 'image'
    
    @property
    def is_video(self):
        return self.media_type == 'video'
    
    def get_file_size_display(self):
        # просмотр размера файла в читаемом формате
        if not self.file_size:
            return "Unknown"
        
        size = self.file_size
        for unit in ['bytes', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)  
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.content[:15], self.name)
    