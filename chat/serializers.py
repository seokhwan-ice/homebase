from rest_framework import serializers

from .models import ChatRoom

# from user.models import User


# # Creator
# class CreatorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["nickname", "profile_image"]


class ChatRoomSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = ChatRoom
        fields = ["id", "name", "image", "creator", "created_at"]
        read_only_fields = ["id", "creator", "created_at"]
