from django import forms
from .models import MyUser
from django.contrib.auth.hashers import make_password  

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Name',
        'title': 'Type your name',
        'required': 'True',
        'class': 'custom-input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'title': 'Type new password',
        'required': 'True',
        'class': 'custom-input'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'title': 'Type your email',
        'required': 'True',
        'class': 'custom-input'
    }))
    birthdate = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'id': 'reg-birthdate',
        'min': '1900-01-01',
        'max': '2025-01-01',
        'placeholder': 'yyyy-mm-dd',
    }), input_formats=["%Y-%m-%d"])   
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'birthdate']

    def save(self, commit=True):
        user = super().save(commit=False)  
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()  
        return user

class SignInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Name',
        'title': 'Type your name',
        'required': 'True',
        'class': 'custom-input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'title': 'Type your password',
        'required': 'True',
        'class': 'custom-input'
    }))
