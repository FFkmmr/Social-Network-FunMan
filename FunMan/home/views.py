from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from .forms import PostForm
from .models import Post 


def profile(request):
    posts = Post.objects.filter(user=request.user).order_by("-date")

    return render(request, "home/profile.html", {"posts": posts})


@login_required
def home(request):
    posts = Post.objects.filter(user=request.user).order_by("-date")
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("home")  
    else:
        form = PostForm()
    return render(request, "home/home.html", {"form": form, "posts": posts})


# @login_required
# def profile(request):
#     user = request.user
    
#     context = {
#         "user" : user
#     }
#     return render(request, "home/profile.html", context)


@login_required
def bookmarks(request):
    return render(request, "home/bookmarks.html")


@login_required
def community(request):
    return render(request, "home/communities.html")


@login_required
def lists(request):
    return render(request, "home/lists.html")


@login_required
def messages(request):
    return render(request, "home/messages.html")

