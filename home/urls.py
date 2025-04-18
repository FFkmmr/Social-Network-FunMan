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
    
]
