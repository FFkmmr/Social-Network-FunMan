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















from django.contrib import messages
from .forms import SetPasswordForm
from authorization.models import MyUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseForbidden
from .utils import generate_token, decode_token
from django.utils.encoding import force_str


def password_reset(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = MyUser.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(force_bytes(user.id))
                token = generate_token(user.id)

                reset_url = request.build_absolute_uri(f'/authorization/reset/{uidb64}/{token}/')
                
                send_mail(
                    'Reset your password',
                    f'Hello! To reset your password, click the link below:\n{reset_url}',
                    'funman1@gmail.com',
                    [email],
                )
                return redirect('login')
            except MyUser.DoesNotExist:
                form.add_error('email', 'User with this email does not exist.')
    else:
        form = EmailForm()
    return render(request, 'authorization/change_password.html', {'form': form})


def change_password(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    
    if user is not None:
        user_id = decode_token(token)
        if user_id and user_id == user.id: 
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('login')
            else:
                form = SetPasswordForm(user)
            return render(request, 'authorization/password_reset_form.html', {'form': form})
        else:
            return redirect('login')
    else:
        return redirect('login')
    
