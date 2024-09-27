from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Free, Live, Comment
from . import serializers


# Free, Live 공통 로직
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]  # TODO: 권한 논의 후 수정

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # 작성자=현재유저

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied("본인의 글만 수정할 수 있습니다!")
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("본인의 글만 삭제할 수 있습니다!")
        instance.delete()

    # 댓글 수정/삭제 공통로직 # TODO: 댓글기능 오류 있는지 이것저것 실험해줘..
    def get_comment(self, request, instance):
        comment_id = request.data.get("comment_id")
        try:
            comment = Comment.objects.get(
                id=comment_id,
                object_id=instance.id,
                content_type=ContentType.objects.get_for_model(self.get_model()),
            )
        except Comment.DoesNotExist:
            raise NotFound("해당 댓글을 찾을 수 없음")
        if comment.author != request.user:
            raise PermissionDenied("본인의 댓글만 수정/삭제할 수 있음")
        return comment

    # 대/댓글 등록
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def create_comment(self, request, pk=None):
        instance = self.get_object()
        parent_id = request.data.get("parent")

        parent_comment = None
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                return Response(
                    data={"error": "해당 부모 댓글을 찾을 수 없음"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        serializer = serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=request.user,
                content_type=ContentType.objects.get_for_model(self.get_model()),
                object_id=instance.id,
                parent=parent_comment,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 수정
    @action(detail=True, methods=["put"], permission_classes=[IsAuthenticated])
    def update_comment(self, request, pk=None):
        instance = self.get_object()
        comment = self.get_comment(request, instance)
        serializer = serializers.CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 삭제
    @action(detail=True, methods=["delete"], permission_classes=[IsAuthenticated])
    def delete_comment(self, request, pk=None):
        instance = self.get_object()
        comment = self.get_comment(request, instance)
        comment.delete()
        return Response(data={"detail": "삭제완료!"}, status=status.HTTP_204_NO_CONTENT)


class FreeViewSet(BaseViewSet):
    queryset = Free.objects.all()

    def get_queryset(self):
        queryset = Free.objects.all()
        search = self.request.query_params.get("q")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )  # TODO: 쿼리호출결과 확인해보고 감당안되면 제목만 검색하자요
        return queryset

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return serializers.FreeCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return serializers.FreeListSerializer  # Read:list
        elif self.action in ["retrieve", "destroy"]:
            return serializers.FreeDetailSerializer  # Read:detail, Delete

    def get_model(self):
        return Free


class LiveViewSet(BaseViewSet):
    queryset = Live.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return serializers.LiveCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return serializers.LiveListSerializer  # Read:list
        elif self.action in ["retrieve", "destroy"]:
            return serializers.LiveDetailSerializer  # Read:detail, Delete

    def get_model(self):
        return Live
