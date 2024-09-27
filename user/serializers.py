from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "name",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["profile_image", "nickname", "bio", "created_at"]


# 추가적인 커뮤니티, 코멘트, 좋아요 구현 후 필드추가.


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone_number", "nickname", "bio"]


# account- 내 계정(개인정보) 수정 페이지 추후 비번필드도 보여줌?
