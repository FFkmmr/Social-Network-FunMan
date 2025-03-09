from django.contrib import admin

from django.contrib import admin
from .models import Post, Comment
# from .models import  NewComment

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'date')
    search_fields = ('user', 'content')
    list_filter = ('date', 'user', 'tags')
    prepopulated_fields = {"slug": ("user",)}

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
# admin.site.register(NewComment)
