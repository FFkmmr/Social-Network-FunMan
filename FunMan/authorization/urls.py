from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.authoriz_moment, name="main_page"),
    path('rules/', views.rules, name='rules'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
    path('accounts/', include('allauth.urls')),
    path('change-password/', views.change_password, name='change_password'),
    
    path('password_reset/', views.password_reset, name='password_reset'),

]
    # http://127.0.0.1:8000/authorization/change-password/