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

    def get_replies(self, instance):
        if instance.replies.exists():
            return CommentSerializer(instance.replies.all(), many=True).data
        return None

    def get_likes_count(self, instance):
        return instance.likes_count

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
        fields = ["title", "content", "free_image"]


class FreeListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Free
        fields = ["id", "author", "title", "comments_count"]

    def get_comments_count(self, instance):
        content_type = ContentType.objects.get_for_model(Free)
        return Comment.objects.filter(
            content_type=content_type, object_id=instance.id
        ).count()


class FreeDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

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
            "comments_count",
            "comments",
        ]

    def get_comments(self, instance):
        content_type = ContentType.objects.get_for_model(Free)
        comments = Comment.objects.filter(
            content_type=content_type, object_id=instance.id, parent__isnull=True
        )
        return CommentSerializer(comments, many=True).data

    def get_comments_count(self, instance):
        content_type = ContentType.objects.get_for_model(Free)
        return Comment.objects.filter(
            content_type=content_type, object_id=instance.id
        ).count()


# Live
class LiveCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = ["title", "content", "live_image", "game_date", "seat", "team"]


class LiveListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Live
        fields = [
            "id",
            "author",
            "title",
            "live_image",
            "likes_count",
            "comments_count",
        ]

    def get_likes_count(self, instance):
        return instance.likes_count

    def get_comments_count(self, instance):
        content_type = ContentType.objects.get_for_model(Live)
        return Comment.objects.filter(
            content_type=content_type, object_id=instance.id
        ).count()


class LiveDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

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
            "comments_count",
            "comments",
        ]

    def get_comments(self, instance):
        content_type = ContentType.objects.get_for_model(Live)
        comments = Comment.objects.filter(
            content_type=content_type, object_id=instance.id, parent__isnull=True
        )
        return CommentSerializer(comments, many=True).data

    def get_likes_count(self, instance):
        return instance.likes_count

    def get_comments_count(self, instance):
        content_type = ContentType.objects.get_for_model(Live)
        return Comment.objects.filter(
            content_type=content_type, object_id=instance.id
        ).count()
