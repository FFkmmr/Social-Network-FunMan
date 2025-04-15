from django.utils.timezone import now
from datetime import timedelta
from django.utils.text import slugify
import random

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