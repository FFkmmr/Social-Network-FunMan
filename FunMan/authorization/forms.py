from django import forms
from .models import MyUser
from django.contrib.auth.hashers import make_password  
from django.contrib.auth import get_user_model

User = get_user_model()


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


class EmailForm(forms.Form):
    email = forms.EmailField(label='Enter your email', required=True)

    
class SetPasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user
