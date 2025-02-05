from django.urls import path
from . import views

urlpatterns = [
    path("", views.authoriz_moment, name="main_page"),
]
 