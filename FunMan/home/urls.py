from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('messages/', views.messages, name="messages"),
    path('bookmarks/', views.bookmarks, name="bookmarks"),
    path('profile/', views.profile, name="profile"),
    path('community/', views.community, name="community"),
    path('lists/', views.lists, name="lists"),
]
