from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import (
    ChatSession, ChatSessionMember, ChatSessionMessage, deserialize_user
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import ChatSessionSerializer, UserSerializer, ChatSessionMemberSerializer

#Forms
from .chatRoom_form import chatroomForm

class UsersView(APIView):
    #User Must Be Authenticated To do anything
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
        

class ChatSessionView(APIView):
    """Manage Chat sessions."""
    #User Must Be Authenticated To do anything
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # We Want To get All Chat Rooms Created by the Authenticated user
        rooms = ChatSession.objects.all()
        members = ChatSessionMember.objects.all()
        members_serializer = ChatSessionMemberSerializer(members, many=True)
        serializer = ChatSessionSerializer(rooms, many=True)
        return Response({ 'rooms': serializer.data, 'members': members_serializer.data })

    def post(self, request, *args, **kwargs):
        """create a new chat session."""
        user = request.user

        roomName = request.data['room']
        roomtype = request.data['type']

        chat_session = ChatSession.objects.create(owner=user, name=roomName, room_type=roomtype)
        
        if roomtype == 'r': # Add The other user in the private chat On creating the chatroom
            chatWith = request.data['chatWith']
            usertoAdd = User.objects.get(username=chatWith)
            
            chat_session = ChatSession.objects.get(uri=chat_session.uri)
            owner = chat_session.owner
            if owner != chatWith:
                chat_session.members.get_or_create(user=usertoAdd, chat_session=chat_session)

        return Response({
            'status': 'SUCCESS', 'uri': chat_session.uri,
            'message': 'New chat session created'
        })

    def patch(self, request, *args, **kwargs):
        """Add a user to a chat session."""
        User = get_user_model()

        uri =  kwargs['uri']
        username = request.data['username']
        roomtype = request.data['type']
        user = User.objects.get(username=username)

        chat_session = ChatSession.objects.get(uri=uri)
        owner = chat_session.owner

        if owner != user:  # Only allow non owners join the room  
            if roomtype == 'p': # Only Add members to public rooms   
                chat_session.members.get_or_create(user=user, chat_session=chat_session)

        owner = deserialize_user(owner)
        members = [
            deserialize_user(chat_session.user) 
            for chat_session in chat_session.members.all()
        ]
        members.insert(0, owner)  # Make the owner the first member

        return Response ({
            'status': 'SUCCESS', 'members': members,
            'message': '%s joined that chat' % user.username,
            'user': deserialize_user(user)
        }) 
   
class ChatSessionMessageView(APIView):
    """Create/Get Chat session messages."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """return all messages in a chat session."""
        uri = kwargs['uri']

        chat_session = ChatSession.objects.get(uri=uri)
        messages = [chat_session_message.to_json() 
            for chat_session_message in chat_session.messages.all()]

        return Response({
            'id': chat_session.id, 'uri': chat_session.uri,
            'messages': messages
        })

    
    def post(self, request, *args, **kwargs):
        """create a new message in a chat session."""
        uri = kwargs['uri']
        message = request.data['message']
        message_type = request.data['type']

        user = request.user
        chat_session = ChatSession.objects.get(uri=uri)

        ChatSessionMessage.objects.create(
            user=user, chat_session=chat_session, message=message , message_type = message_type
        )

        return Response ({
            'status': 'SUCCESS', 'uri': chat_session.uri, 'message': message, 'type': message_type,
            'user': deserialize_user(user)
        })
