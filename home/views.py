from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm
from .models import Post
from authorization.models import Message, Chat
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
    

@login_required
def messages(request):
    user = request.user
    chats = user.chats.all()
    filter_id = request.GET.get('filter')

    chats_with_partners = [
        (chat, chat.participants.exclude(id=user.id).first(), chat.messages.order_by('-timestamp').first())
        for chat in chats
    ]

    selected_chat = chats.filter(id=filter_id).first() if filter_id else None
    selected_chat_partner = selected_chat.participants.exclude(id=user.id).first() if selected_chat else None

    if request.method == 'POST' and selected_chat:
        message_text = request.POST.get('message', '').strip()
        if message_text:
            Message.objects.create(chat=selected_chat, sender=user, text=message_text)
            return redirect(f"{request.path}?filter={selected_chat.id}")

    return render(request, "home/messages.html", {
        'user': user,
        'usersA': User.objects.all(),
        'chats_with_partners': chats_with_partners,
        'selected_chat': selected_chat,
        'selected_chat_partner': selected_chat_partner,
    })


def new_message(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'home/new_message.html', context)


def filter_users(request):
    search = request.GET.get('search', '')
    users = User.objects.filter(username__icontains=search)
    return JsonResponse({
        'users': list(users.values('id', 'username'))  
    })


def new_chat(request, user_id):

    target_user = get_object_or_404(User, id=user_id)
    chats = Chat.objects.filter(participants=request.user).filter(participants=target_user)

    if chats.exists():
        chat = chats.first()
    else:
        chat = Chat.objects.create()
        chat.participants.add(request.user, target_user)

    return redirect(f'/messages/?filter={chat.id}')


def get_users(request):
    users = list(User.objects.values('id', 'username'))
    return JsonResponse(users, safe=False)


def delete_chat(request, user_id):
    chat = Chat.objects.filter(participants=request.user).filter(participants__id=user_id).first()    
    if chat:
        chat.delete()
        
    return redirect('messages')
