from django.utils.timezone import now
from datetime import timedelta
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import random
import os

User = get_user_model()


def time_since_post(post_date):
    delta = now() - post_date

    if delta < timedelta(minutes=1):
        return "только что"
    elif delta < timedelta(hours=1):
        return f"{delta.seconds // 60} мин назад"
    elif delta < timedelta(days=1):
        return f"{delta.seconds // 3600} ч {delta.seconds % 3600 // 60} мин назад"
    elif delta < timedelta(weeks=1):
        return f"{delta.days} д {delta.seconds // 3600} ч назад"
    else:
        return post_date.strftime("%d.%m.%Y %H:%M")


def generate_slug(user, content):
    base_slug = slugify(f"{user}-{content[:10]}")
    return f"{base_slug}-{random.randint(1000, 9999)}"


def like_or_not(request, posts):
    for post in posts:
        post.is_something_by_user = post.is_liked_by(request.user)


def following_posts(request, posts):
    user = request.user
    followed_users = user.following.all()
    return posts.exclude(user=user).filter(user__in=followed_users)


def process_uploaded_media(post, files):
    """Обрабатывает загруженные медиа файлы с валидацией"""
    from .models import MediaFile
    
    allowed_image_ext = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    allowed_video_ext = ['.mp4', '.mov', '.webm']
    max_image_size = 10 * 1024 * 1024    # 10MB
    max_video_size = 300 * 1024 * 1024   # 300MB
    
    for file in files:
        # Валидация расширения файла
        ext = os.path.splitext(file.name)[1].lower()
        
        if ext in allowed_image_ext:
            if file.size > max_image_size:
                raise ValueError(f'Image file {file.name} is too large. Maximum size is 10MB.')
        elif ext in allowed_video_ext:
            if file.size > max_video_size:
                raise ValueError(f'Video file {file.name} is too large. Maximum size is 300MB.')
        else:
            raise ValueError(f'File type {ext} is not supported.')
        
        MediaFile.objects.create(
            post=post,
            file=file
        )


def get_posts_by_filter(user, filter_type):
    """Получает посты по типу фильтра"""
    from .models import Post
    
    if filter_type == 'posts':
        return Post.objects.filter(user=user).prefetch_related('media').order_by("-date")
    elif filter_type == 'replies':
        return Post.objects.filter(comments__name=user).distinct().prefetch_related('media').order_by("-date")
    elif filter_type == 'media':
        return Post.objects.filter(user=user, media__isnull=False).distinct().prefetch_related('media').order_by("-date")
    elif filter_type == 'likes':
        return Post.objects.filter(likes=user).prefetch_related('media').order_by("-date")
    else:
        return Post.objects.filter(user=user).prefetch_related('media').order_by("-date")


def toggle_like_service(request, post_id):
    """Сервис для переключения лайка поста"""
    from .models import Post
    
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})


def create_comment_service(request, post_id):
    """Сервис для создания комментария"""
    from .models import Post
    from .forms import CommentForm
    
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user
            comment.save()
            return True
    
    return False


def create_post_service(request, form):
    """Сервис для создания поста"""
    try:
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        post.tags.set(form.cleaned_data["tags"])
        
        # Обрабатываем загруженные файлы
        files = request.FILES.getlist('media_files')
        if files:
            process_uploaded_media(post, files)
        
        return True, None
    except ValueError as e:
        return False, str(e)


def toggle_follow_service(request, user_id):
    """Сервис для подписки/отписки"""
    target = User.objects.get(id=user_id)
    if target in request.user.following.all():
        request.user.following.remove(target)
        following = False
    else:
        request.user.following.add(target)
        following = True
    
    return JsonResponse({"following": following})


def get_chats_data(user, filter_id):
    """Получает данные для чатов"""
    from authorization.models import Chat
    
    chats = user.chats.all()
    
    chats_with_partners = [
        (chat, chat.participants.exclude(id=user.id).first(), chat.messages.order_by('-timestamp').first())
        for chat in chats
    ]
    
    selected_chat = chats.filter(id=filter_id).first() if filter_id else None
    selected_chat_partner = selected_chat.participants.exclude(id=user.id).first() if selected_chat else None
    
    return {
        'chats_with_partners': chats_with_partners,
        'selected_chat': selected_chat,
        'selected_chat_partner': selected_chat_partner
    }


def create_message_service(user, selected_chat, message_text):
    """Создает сообщение в чате"""
    from authorization.models import Message
    
    if message_text.strip():
        Message.objects.create(chat=selected_chat, sender=user, text=message_text)
        return True
    return False


def get_or_create_chat(request_user, target_user_id):
    """Получает существующий чат или создает новый"""
    from authorization.models import Chat
    
    target_user = get_object_or_404(User, id=target_user_id)
    chats = Chat.objects.filter(participants=request_user).filter(participants=target_user)
    
    if chats.exists():
        chat = chats.first()
    else:
        chat = Chat.objects.create()
        chat.participants.add(request_user, target_user)
    
    return chat


def delete_chat_service(request_user, user_id):
    """Удаляет чат с пользователем"""
    from authorization.models import Chat
    
    chat = Chat.objects.filter(participants=request_user).filter(participants__id=user_id).first()
    if chat:
        chat.delete()
        return True
    return False
    