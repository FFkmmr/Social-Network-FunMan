from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm, SignInForm, EmailForm
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail


def authoriz_moment(request):
    return render(request, "authorization/index.html")


def rules(request):
    return render(request, "authorization/rules.html")


def login_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(reverse('home'))
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = SignInForm()
    return render(request, "authorization/login.html", {'form': form})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            auth_login(request, user)
            return redirect('home') 
    else:
        form = RegistrationForm()
    return render(request, "authorization/registration.html", {'form': form})















from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes

def change_password(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            user = request.user
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = f"http://127.0.0.1:8000/password_reset/{uid}/{token}/"

            send_mail(
                'Reset your password',
                f'Hello! To reset your password, click the link below:\n{reset_url}',
                'funman1@gmail.com',
                [email],
            )
            messages.success(request, 'Email with password reset link has been sent!')
            return redirect('home')
    else:
        form = EmailForm()

    return render(request, "authorization/change_password.html", {'form': form})


def password_reset(request):
    print("ЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙ")
    try:

        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data["new_password1"]
                user.set_password(new_password)
                user.save()

                messages.success(request, "Your password has been successfully reset.")
                return redirect('home')
        else:
            form = SetPasswordForm()

        return render(request, 'authorization/password_reset_form.html', {'form': form})
    else:
        messages.error(request, "The password reset link is invalid or expired.")
        return redirect('home')
    