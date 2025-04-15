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
    
]
