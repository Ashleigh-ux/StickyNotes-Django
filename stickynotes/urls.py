"""
URL configuration for the Sticky Notes app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_note, name='add_note'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
]
