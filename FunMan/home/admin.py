from django.contrib import admin

from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'date')
    search_fields = ('user', 'content')
    list_filter = ('date', 'user', 'tags')
    prepopulated_fields = {"slug": ("user",)}
    filter_horizontal = ('comments',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
