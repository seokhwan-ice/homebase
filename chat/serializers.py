from rest_framework import serializers
from .models import ChatRoom, ChatMessage


# 채팅방
class ChatRoomSerializer(serializers.ModelSerializer):
    # 참여자 수
    participants_count = serializers.IntegerField(
        source="participants.count", read_only=True
    )
    # 마지막 메시지 시간
    latest_message_time = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "title",
            "image",
            "description",
            "creator",
            "created_at",
            "participants_count",
            "latest_message_time",
        ]
        read_only_fields = ["creator", "created_at"]

    def get_latest_message_time(self, obj):
        last_message = obj.messages.order_by("-created_at").first()
        if last_message:
            return last_message.created_at
        return "메시지 없음"


# 채팅 메시지
class ChatMessageSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source="user.nickname")

    class Meta:
        model = ChatMessage
        fields = ["id", "room", "user_nickname", "content", "created_at"]
