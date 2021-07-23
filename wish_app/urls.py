from django.contrib import admin
from django.urls import path, include
from wish_app import views

urlpatterns = [
    path('', views.index),
    path('wishes', views.wishes),
    path('wishes/new', views.new_wish),
    path('wishes/stats', views.stats),
    path('wishes/granted/<int:wish_id>', views.grant_wish),
    path('wishes/remove/<int:wish_id>', views.remove_wish),
    path('wishes/edit/<int:wish_id>', views.edit_wish),
    path('wishes/like/<int:wish_id>', views.like_wish),
    path('logout', views.logout),
]