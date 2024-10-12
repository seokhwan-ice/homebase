from rest_framework import serializers
from .models import ChatRoom, ChatMessage


# 채팅방
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ["id", "title", "image", "description", "creator", "created_at"]
        read_only_fields = ["creator", "created_at"]


# 채팅 메시지
class ChatMessageSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source="user.nickname")

    class Meta:
        model = ChatMessage
        fields = ["id", "room", "user_nickname", "content", "created_at"]
