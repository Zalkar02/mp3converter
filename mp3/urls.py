from django.contrib import admin
from django.urls import path

from mp3site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base, name='base')
]
