from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, "home/home.html")


@login_required
def profile(request):
    return render(request, "home/profile.html")


@login_required
def bookmarks(request):
    return render(request, "home/bookmarks.html")


@login_required
def communities(request):
    return render(request, "home/communities.html")


@login_required
def lists(request):
    return render(request, "home/lists.html")


@login_required
def messages(request):
    return render(request, "home/messages.html")

