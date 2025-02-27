from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Let\'s type something',
        'title': 'Content',
        'required': 'True',
        'class': 'custom-input'
    }))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Tags',
        'title': 'Some tags maybe?',
        'class': 'custom-input'
    }))
    
    class Meta:
        model = Post
        fields = ['content', 'tags']
    