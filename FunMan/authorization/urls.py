from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.authoriz_moment, name="main_page"),
    path('rules/', views.rules, name='rules'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
]
    