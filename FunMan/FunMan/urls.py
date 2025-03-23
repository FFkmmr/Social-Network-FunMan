from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authorization/', include("authorization.urls")),
    path('', include("home.urls")),
    path('accounts/', include('allauth.urls')),
    path('reset/', include('authorization.urls')),
]
