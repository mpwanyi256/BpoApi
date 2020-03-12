from .models import ChatSession
from django import forms

class chatroomForm(forms.ModelForm):

    class Meta:
        model = ChatSession
        fields = ['name']