from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    
    def __str__(self):
        return self.username
