from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('messages/', views.messages, name="messages"),
    path('bookmarks/', views.bookmarks, name="bookmarks"),
    path('profile/', views.profile, name="profile"),
    path('community/', views.community, name="community"),
    path('lists/', views.lists, name="lists"),
    path('toggle-like/<int:post_id>/', views.toggle_like, name='toggle_like'),

    # path('write-comment/<int:post_id>/', views.write_comment, name='write_comment'),
    path('get-comment-form/', views.get_comment_form, name='get_comment_form'),
]
