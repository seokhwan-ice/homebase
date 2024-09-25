from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "name",
            "password",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["profile_image", "nickname", "bio", "created_at"]


# 추가적인 커뮤니티, 코멘트, 좋아요 구현후 필드추가.
