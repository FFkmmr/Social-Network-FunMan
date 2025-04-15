from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from .forms import PostForm, CommentForm
from .models import Post
from .services import like_or_not
from django.http import JsonResponse


@login_required
def profile(request):
    filter_type = request.GET.get('filter', 'posts')   
    
    if filter_type == 'posts':
        posts = Post.objects.filter(user=request.user).order_by("-date")
        like_or_not(request, posts)
    elif filter_type == 'replies': 
        posts = Post.objects.filter(comments__name=request.user).distinct().order_by("-date")
        like_or_not(request, posts)
    elif filter_type == 'media':
        posts = Post.objects.filter(content__icontains='img', user=request.user).order_by("-date")
        like_or_not(request, posts)
    elif filter_type == 'likes':
        posts = Post.objects.filter(likes=request.user).order_by("-date")
        like_or_not(request, posts)
    else:
        posts = Post.objects.filter(user=request.user).order_by("-date")
        like_or_not(request, posts)

    return render(request, "home/profile.html", {"posts": posts, "filter": filter_type})


@login_required
def home(request):
    posts = Post.objects.order_by("-date")
    
    for post in posts:
        post.is_something_by_user = post.is_liked_by(request.user)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            post.tags.set(form.cleaned_data["tags"])
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "home/home.html", {"form": form, "posts": posts})


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user) 
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})


@login_required
def write_comment(request, post_id):
    posts = Post.objects.order_by("-date")
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user
            comment.save()
            return redirect("home")
    else:
        form = CommentForm()
        secform = PostForm()
    return render(request, 'includes/comment_form.html', {'form': form, 'post': post, 'posts': posts, 'secform': secform, 'user': user})


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

