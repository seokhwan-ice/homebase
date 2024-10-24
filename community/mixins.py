from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Comment, Like, Bookmark
from . import serializers


class CommentMixin:
    """
    1) 댓글 생성

        URL경로 -  /<글 모델>/<pk>/create_comment/ (POST)
        필수입력 - "content" : "생성할 댓글 내용"
        선택입력 - "parent_id" : 대댓글을 달고싶다면 부모댓글의 id

    2) 댓글 수정

        URL경로 -  /<글 모델>/<pk>/update_comment/ (PUT)
        필수입력 - "comment_id" : 수정할 대.댓글의 id
        선택입력 - "content" : "수정된 대.댓글 내용"

    3) 댓글 삭제

        URL경로 -  /<글 모델>/<pk>/delete_comment/ (DELETE)
        필수입력 - "comment_id" : 삭제할 대.댓글의 id
    """

    def get_comment(self, request, instance):  # 댓글 수정/삭제 공통로직
        comment_id = request.data.get("comment_id")
        try:
            comment = Comment.objects.get(
                id=comment_id,
                content_type=ContentType.objects.get_for_model(self.get_model()),
                object_id=instance.id,
            )
        except Comment.DoesNotExist:
            raise NotFound("해당 댓글을 찾을 수 없음")
        if comment.author != request.user:
            raise PermissionDenied("본인의 댓글만 수정/삭제할 수 있음")
        return comment

    @action(detail=True, methods=["post"])
    def create_comment(self, request, pk=None):
        instance = self.get_object()
        parent_id = request.data.get("parent_id")
        parent_comment = None
        if parent_id:
            try:
                parent_comment = Comment.objects.get(
                    id=parent_id,
                    content_type=ContentType.objects.get_for_model(instance),
                    object_id=instance.id,
                )
            except Comment.DoesNotExist:
                raise NotFound("해당 부모 댓글을 찾을 수 없음")

        serializer = serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=request.user,
                content_type=ContentType.objects.get_for_model(self.get_model()),
                object_id=instance.id,
                parent=parent_comment,
            )
            instance.update_comments_count()  # 댓글수 업데이트
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put"])
    def update_comment(self, request, pk=None):
        instance = self.get_object()
        comment = self.get_comment(request, instance)
        serializer = serializers.CommentSerializer(
            comment, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def delete_comment(self, request, pk=None):
        instance = self.get_object()
        comment = self.get_comment(request, instance)
        comment.delete()
        instance.update_comments_count()  # 댓글수 업데이트
        return Response(data={"detail": "삭제완료!"}, status=status.HTTP_204_NO_CONTENT)


class LikeMixin:
    """
    1) 글 좋아요 & 좋아요 취소

        URL경로 -  /<글 모델>/<pk>/toggle_like_article/ (POST)

    2) 댓글 좋아요 & 좋아요 취소

        URL경로 -  /<글 모델>/<pk>/toggle_like_comment/ (POST)
        필수입력 - "comment_id" : 좋아요 및 취소할 대.댓글의 id
    """

    def toggle_like(self, request, instance):  # 글/댓글 좋아요 공통로직
        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        )
        if not created:
            like.delete()
            instance.update_likes_count()  # 좋아요수 업데이트
            return Response(
                data={"detail": "좋아요 취소됨"}, status=status.HTTP_204_NO_CONTENT
            )
        instance.update_likes_count()  # 좋아요수 업데이트
        return Response(data={"detail": "좋아요!"}, status=status.HTTP_201_CREATED)

    def get_like_status(self, user, instance):
        """좋아요 상태 확인 -> 화면에서 확인할 수 있도록!"""
        return Like.objects.filter(
            user=user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        ).exists()

    @action(detail=True, methods=["post"])
    def toggle_like_article(self, request, pk=None):
        instance = self.get_object()
        return self.toggle_like(request, instance)

    @action(detail=True, methods=["post"])
    def toggle_like_comment(self, request, pk=None):
        instance = self.get_object()
        comment_id = request.data.get("comment_id")
        try:
            comment = Comment.objects.get(
                id=comment_id,
                content_type=ContentType.objects.get_for_model(self.get_model()),
                object_id=instance.id,
            )
        except Comment.DoesNotExist:
            raise NotFound("해당 댓글을 찾을 수 없음")
        return self.toggle_like(request, comment)


class BookmarkMixin:
    """
    1) 글 북마크 & 북마크 취소

        URL경로 -  /<글 모델>/<pk>/toggle_bookmark/ (POST)
    """

    @action(detail=True, methods=["post"])
    def toggle_bookmark(self, request, pk=None):
        instance = self.get_object()
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        )
        if not created:
            bookmark.delete()
            return Response(
                data={"detail": "북마크 취소됨"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(data={"detail": "북마크!"}, status=status.HTTP_201_CREATED)

    def get_bookmark_status(self, user, instance):
        """북마크 상태 확인 -> 화면에서 확인할 수 있도록!"""
        return Bookmark.objects.filter(
            user=user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        ).exists()
