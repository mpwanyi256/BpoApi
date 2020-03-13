from django.contrib import admin
from .models import ChatSession, ChatSessionMessage, ChatSessionMember

# Register your models here.
admin.site.register(ChatSession)
admin.site.register(ChatSessionMessage)
admin.site.register(ChatSessionMember)