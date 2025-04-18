from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm
from .models import Post
from .services import like_or_not, following_posts
from django.http import JsonResponse

User = get_user_model()

def redirect_to_home(request):
    return redirect('home')

@login_required
def home(request):
    filter_type = request.GET.get('filter', 'for_u')
    posts = Post.objects.order_by("-date")

    if filter_type == "following":
        posts = following_posts(request, posts)
    else: 
        posts = Post.objects.order_by("-date")

    like_or_not(request, posts)

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
    return render(request, "home/home.html", {"form": form, "posts": posts, "filter": filter_type})


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

    return render(request, "home/profile.html", {"posts": posts, "filter": filter_type, 'stranger': False, "user": request.user})





@login_required
def stranger_profile(request, user_id):
    filter_type = request.GET.get('filter', 'posts')   
    user = get_object_or_404(User, id=user_id)
    is_following = request.user.following.filter(id=user_id).exists()
    
    if filter_type == 'posts':
        posts = Post.objects.filter(user=user_id).order_by("-date")
        like_or_not(request, posts)
    elif filter_type == 'media':
        posts = Post.objects.filter(content__icontains='img', user=user_id).order_by("-date")
        like_or_not(request, posts)

    if (request.user.id == user_id):
        stranger = False
    else:
        stranger = True
    return render(request, "home/profile.html", {"posts": posts, "filter": filter_type, 'stranger': stranger, 'user': user, "is_following": is_following})




@login_required
def follow_toggle(request, user_id):
    if request.method == "POST":
        target = User.objects.get(id=user_id)
        if target in request.user.following.all():
            request.user.following.remove(target)
            following = False
        else:
            request.user.following.add(target)
            following = True
        return JsonResponse({"following": following})