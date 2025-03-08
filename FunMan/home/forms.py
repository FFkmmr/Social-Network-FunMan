from django import forms
from .models import Post, Comment
from taggit.forms import TagField

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Let\'s type something',
        'title': 'Content',
        'required': 'True',
        'class': 'custom-input',
    }))
    tags = TagField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Tags',
        'title': 'Some tags maybe?',
        'class': 'custom-input'
    }))
    
    class Meta:
        model = Post
        fields = ['content', 'tags']
    
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text']
