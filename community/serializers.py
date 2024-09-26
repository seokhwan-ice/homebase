from rest_framework import serializers
from user.models import User
from .models import Free


# Author
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "profile_image"]  # 작성자에서 가져올 필드


# Create, Update
class FreeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Free
        fields = ["title", "content", "free_image"]


# Read:list
class FreeListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Free
        fields = ["id", "author", "title", "content"]


# Read:detail
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
