from django.contrib import admin
from django.urls import path

from . import views

#Testing Channels
app_name = 'chat'

urlpatterns = [
    path('chats/', views.ChatSessionView.as_view()),
    path('users/', views.UsersView.as_view()),
    path('chats/<uri>/', views.ChatSessionView.as_view()),
    path('chats/<uri>/messages/', views.ChatSessionMessageView.as_view()),
]