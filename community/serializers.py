from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from user.models import User
from .models import Free, Live, Comment


# Author
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "profile_image"]
        # 작성자에서 가져올 필드(나중에 더 추가될거같아서 만든거에요 삭제가능)


# Comment
class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at", "likes_count", "replies"]

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return None

    def get_likes_count(self, obj):
        return obj.likes_count


# Free
class FreeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Free
        fields = ["title", "content", "free_image"]


class FreeListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Free
        fields = ["id", "author", "title"]


# TODO: 댓글 카운트 기능 까먹지말고 넣어야함ㅠㅠ
class FreeDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

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
            "comments",
        ]

    def get_comments(self, obj):
        content_type = ContentType.objects.get_for_model(Free)
        comments = Comment.objects.filter(
            content_type=content_type, object_id=obj.id, parent__isnull=True
        )
        return CommentSerializer(comments, many=True).data


# Live
class LiveCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = ["title", "content", "live_image", "game_date", "seat", "team"]


class LiveListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Live
        fields = ["id", "author", "title", "live_image", "likes_count"]

    def get_likes_count(self, obj):
        return obj.likes_count


class LiveDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

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
            "likes_count",
            "comments",
        ]

    def get_comments(self, obj):
        content_type = ContentType.objects.get_for_model(Live)
        comments = Comment.objects.filter(
            content_type=content_type, object_id=obj.id, parent__isnull=True
        )
        return CommentSerializer(comments, many=True).data

    def get_likes_count(self, obj):
        return obj.likes_count
