from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.authoriz_moment, name="main_page"),
    path('rules/', views.rules, name='rules'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
    path('accounts/', include('allauth.urls')),
    
    path('reset/<str:token>/', views.change_password, name='change_password'),
    path('password_reset/', views.password_reset, name='password_reset'),
    # TEST
    # path(
    #     'change-password/',
    #     auth_views.PasswordResetView.as_view(template_name='authorization/reset/password_reset.html'),
    #     name="password_reset"
    # ),
    # path(
    #     'change-password/sent/',
    #     auth_views.PasswordResetDoneView.as_view(template_name='authorization/reset/password_reset_sent.html'),
    #     name="password_reset_done"
    # ),
    # path(
    #     'reset/<uidb64>/<token>/',
    #     auth_views.PasswordResetConfirmView.as_view(template_name='authorization/reset/password_reset_form.html'),
    #     name="password_reset_confirm"
    # ),
    # path(
    #     'change-password_complete/',
    #     auth_views.PasswordResetCompleteView.as_view(template_name='authorization/reset/password_reset_done.html'),
    #     name="password_reset_complete"
    # ),

]
