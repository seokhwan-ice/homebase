from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from user.models import User
from .models import Free, Live, Comment


# Author
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "profile_image"]


# Comment
class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at", "likes_count", "replies"]

    def get_replies(self, instance):
        if instance.replies.exists():
            return CommentSerializer(instance.replies.all(), many=True).data
        return None

    # TODO: 프론트가서 확인해보고 free에도 좋아요 기능할거면 이 함수 삭제
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.content_type.model == "free":
            ret.pop("likes_count", None)
        return ret


# Free
class FreeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Free
        fields = ["id", "title", "content", "free_image"]


class FreeListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    views = serializers.IntegerField(read_only=True)

    class Meta:
        model = Free
        fields = ["id", "author", "title", "views", "comments_count"]


class FreeDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    views = serializers.IntegerField(read_only=True)

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
            "views",
            "comments_count",
            "comments",
        ]

    def get_comments(self, instance):
        content_type = ContentType.objects.get_for_model(Free)
        comments = Comment.objects.filter(
            content_type=content_type, object_id=instance.id, parent__isnull=True
        )
        return CommentSerializer(comments, many=True).data


# Live
class LiveCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = [
            "id",
            "live_image",
            "review",
            "game_date",
            "home_team",
            "away_team",
            "stadium",
            "seat",
        ]


class LiveListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Live
        fields = [
            "id",
            "home_team",
            "away_team",
            "author",
            "stadium",
            "created_at",
            "live_image",
            "likes_count",
            "comments_count",
        ]


class LiveDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Live
        fields = [
            "id",
            "author",
            "stadium",
            "seat",
            "live_image",
            "game_date",
            "home_team",
            "away_team",
            "review",
            "created_at",
            "likes_count",
            "comments_count",
            "comments",
        ]

    def get_comments(self, instance):
        content_type = ContentType.objects.get_for_model(Live)
        comments = Comment.objects.filter(
            content_type=content_type, object_id=instance.id, parent__isnull=True
        )
        return CommentSerializer(comments, many=True).data
