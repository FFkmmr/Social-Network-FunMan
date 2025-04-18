from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.authoriz_moment, name="main_page"),
    path('rules/', views.rules, name='rules'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
    path('reset/<str:token>/', views.change_password, name='change_password'),
    path('password_reset/', views.password_reset, name='password_reset'),

]
