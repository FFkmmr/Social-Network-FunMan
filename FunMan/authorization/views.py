from django.shortcuts import render, redirect
from .forms import RegistrationForm, SignInForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required


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
                return redirect('home')
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

@login_required
def home(request):
    return render(request, "authorization/home.html")