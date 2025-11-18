from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .forms import PostForm, CommentForm
from .models import Post
from .services import (
    like_or_not, following_posts, create_post_service,
    get_posts_by_filter, toggle_like_service, create_comment_service,
    toggle_follow_service, get_chats_data, create_message_service,
    get_or_create_chat, delete_chat_service
)

User = get_user_model()


def redirect_to_home(request):
    return redirect('home')


@login_required
def home(request):
    filter_type = request.GET.get('filter', 'for_u')
    posts = Post.objects.select_related('user').prefetch_related('media', 'likes', 'comments').order_by("-date")

    if filter_type == "following":
        posts = following_posts(request, posts)
    else: 
        posts = Post.objects.select_related('user').prefetch_related('media', 'likes', 'comments').order_by("-date")

    like_or_not(request, posts)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            success, error = create_post_service(request, form)
            if success:
                return redirect("home")
            else:
                form.add_error('media_files', error)
    else:
        form = PostForm()
        
    return render(request, "home/home.html", {"form": form, "posts": posts, "filter": filter_type})


@login_required
def toggle_like(request, post_id):
    return toggle_like_service(request, post_id)


@login_required
def write_comment(request, post_id):
    posts = Post.objects.order_by("-date")
    post = get_object_or_404(Post, id=post_id)
    
    if create_comment_service(request, post_id):
        return redirect("home")
    
    form = CommentForm()
    secform = PostForm()
    return render(request, 'includes/comment_form.html', {
        'form': form, 'post': post, 'posts': posts, 'secform': secform, 'user': request.user
    })


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
def profile(request):
    filter_type = request.GET.get('filter', 'posts')
    posts = get_posts_by_filter(request.user, filter_type)
    like_or_not(request, posts)
    
    return render(request, "home/profile.html", {
        "posts": posts, "filter": filter_type, 'stranger': False, "user": request.user
    })


@login_required
def stranger_profile(request, user_id):
    filter_type = request.GET.get('filter', 'posts')
    user = get_object_or_404(User, id=user_id)
    is_following = request.user.following.filter(id=user_id).exists()
    
    if filter_type == 'posts':
        posts = Post.objects.filter(user=user_id).prefetch_related('media').order_by("-date")
        like_or_not(request, posts)
    elif filter_type == 'media':
        posts = Post.objects.filter(user=user_id, media__isnull=False).distinct().prefetch_related('media').order_by("-date")
        like_or_not(request, posts)

    else:
        posts = Post.objects.filter(user=user_id).prefetch_related('media').order_by("-date")
        
    like_or_not(request, posts)
    
    return render(request, "home/profile.html", {
        "posts": posts, "filter": filter_type, 'stranger': request.user.id != user_id,
        'user': user, "is_following": is_following
    })


@login_required
def follow_toggle(request, user_id):
    if request.method == "POST":
        return toggle_follow_service(request, user_id)


@login_required
def messages(request):
    filter_id = request.GET.get('filter')
    chat_data = get_chats_data(request.user, filter_id)
    
    if request.method == 'POST' and chat_data['selected_chat']:
        message_text = request.POST.get('message', '')
        if create_message_service(request.user, chat_data['selected_chat'], message_text):
            return redirect(f"{request.path}?filter={chat_data['selected_chat'].id}")
    
    return render(request, "home/messages.html", {
        'user': request.user,
        'usersA': User.objects.all(),
        **chat_data
    })


def new_message(request):
    return render(request, 'home/new_message.html', {'users': User.objects.all()})


def filter_users(request):
    search = request.GET.get('search', '')
    users = User.objects.filter(username__icontains=search)
    return JsonResponse({'users': list(users.values('id', 'username'))})


def new_chat(request, user_id):
    chat = get_or_create_chat(request.user, user_id)
    return redirect(f'/messages/?filter={chat.id}')


def get_users(request):
    users = list(User.objects.values('id', 'username'))
    return JsonResponse(users, safe=False)


def delete_chat(request, user_id):
    delete_chat_service(request.user, user_id)
    return redirect('messages')
