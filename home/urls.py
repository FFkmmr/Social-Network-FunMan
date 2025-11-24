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
    path('<int:post_id>/comment', views.write_comment, name='add_comment'),
    path('stranger_profile/<int:user_id>/', views.stranger_profile, name='stranger_profile'),
    path('stranger_profile/', views.redirect_to_home, name='redirect_to_home'),
    path("follow/<int:user_id>/", views.follow_toggle, name="follow_toggle"),
    path("new_message/", views.new_message, name="new_message"),
    path('filter_users/', views.filter_users, name='filter_users'),
    path('new_chat/<int:user_id>', views.new_chat, name='new_chat'),
    path('get_users/', views.get_users, name='get_users'),
    path('delete_chat/<int:user_id>', views.delete_chat, name='delete_chat'),
    path('validate_recipient/', views.validate_message_recipient, name='validate_recipient'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]
