from rest_framework import permissions, serializers
from .models import (
    ChatSession, ChatSessionMember, ChatSessionMessage, deserialize_user
)

class ChatSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatSession
        fields = ('__all__')

class ChatSessionMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatSessionMember
        fields = ('__all__')