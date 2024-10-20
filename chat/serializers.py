from rest_framework import serializers
from .models import ChatRoom, ChatMessage


# 채팅 메시지
class ChatMessageSerializer(serializers.ModelSerializer):
    user_profile_image = serializers.ImageField(
        source="user.profile_image", read_only=True
    )
    user_nickname = serializers.ReadOnlyField(source="user.nickname", read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "room",
            "user_nickname",
            "user_profile_image",
            "content",
            "created_at",
        ]


# 채팅방 Create
class ChatRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ["title", "description", "image"]


# 채팅방 List
class ChatRoomListSerializer(serializers.ModelSerializer):
    # 마지막 대화 시각
    latest_message_time = serializers.SerializerMethodField()
    # 참여자 수
    participants_count = serializers.IntegerField(
        source="participants.count", read_only=True
    )

    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "title",
            "image",
            "description",
            "participants_count",
            "latest_message_time",
        ]

    def get_latest_message_time(self, obj):
        last_message = obj.messages.order_by("-created_at").first()
        return last_message.created_at if last_message else "대화 없음"


# 채팅방 Detail
class ChatRoomDetailSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    creator_profile_image = serializers.ImageField(
        source="creator.profile_image", read_only=True
    )
    creator_nickname = serializers.ReadOnlyField(
        source="creator.nickname", read_only=True
    )
    # 참여자 수
    participants_count = serializers.IntegerField(
        source="participants.count", read_only=True
    )

    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "title",
            "image",
            "description",
            "created_at",
            "messages",
            "creator_profile_image",
            "creator_nickname",
            "participants_count",
        ]
        # TODO: 생성일이랑 방장 정보 넣을까말까 고민중. 익명성에 이점 있어서 안넣는것도 좋을듯
