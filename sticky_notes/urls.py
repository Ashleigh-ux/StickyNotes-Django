"""
Main URL configuration for the Sticky Notes project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stickynotes.urls')),  # 👈 links to your app
]
