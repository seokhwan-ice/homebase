from rest_framework import serializers
from user.models import User
from .models import Free, Live


# Author
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "profile_image"]
        # 작성자에서 가져올 필드(나중에 더 추가될거같아서 만든거에요 삭제가능)


# Free
class FreeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Free
        fields = ["title", "content", "free_image"]


class FreeListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Free
        fields = ["id", "author", "title"]


class FreeDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Free
        fields = [
            "id",
            "author",
            "title",
            "content",
            "free_image",
            "created_at",
            "updated_at",
        ]


# Live
class LiveCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = ["title", "content", "live_image", "game_date", "seat", "team"]


class LiveListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Live
        fields = ["id", "author", "title", "live_image"]


class LiveDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Live
        fields = [
            "id",
            "author",
            "title",
            "content",
            "live_image",
            "game_date",
            "seat",
            "team",
            "created_at",
            "updated_at",
        ]
