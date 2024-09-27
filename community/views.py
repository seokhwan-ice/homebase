from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied  # 403_FORBIDDEN
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Free, Live, Comment
from . import serializers


# Free, Live, Comment 공통 로직
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


class FreeViewSet(BaseViewSet):
    queryset = Free.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return serializers.FreeCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return serializers.FreeListSerializer  # Read:list
        elif self.action in ["retrieve", "destroy"]:
            return serializers.FreeDetailSerializer  # Read:detail, Delete


class LiveViewSet(BaseViewSet):
    queryset = Live.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return serializers.LiveCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return serializers.LiveListSerializer  # Read:list
        elif self.action in ["retrieve", "destroy"]:
            return serializers.LiveDetailSerializer  # Read:detail, Delete


class CommentViewSet(BaseViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return super().get_queryset()

        # query parameter >>> ? type = 게시글유형 & id = 게시글id
        type_str = self.request.GET.get("type")

        if type_str == "free":
            model = Free
        elif type_str == "live":
            model = Live
        else:
            raise ValueError("유효하지 않은 게시글 유형입니다!")

        content_type = ContentType.objects.get_for_model(model)
        object_id = self.request.GET.get("id")

        # 해당 글의 댓글(대댓글x)만 필터링
        return Comment.objects.filter(
            content_type=content_type, object_id=object_id, parent__isnull=True
        )

    def perform_create(self, serializer):
        type_str = self.request.data.get("type")

        if type_str == "free":
            model = Free
        elif type_str == "live":
            model = Live
        else:
            raise ValueError("유효하지 않은 게시글 유형입니다!")

        content_type = ContentType.objects.get_for_model(model)
        object_id = self.request.data.get("id")

        # parent 필드를 가져와서 대댓글인지 확인
        parent_id = self.request.data.get("parent")
        parent = None
        if parent_id:
            parent = Comment.objects.get(id=parent_id)

        serializer.save(
            author=self.request.user,
            content_type=content_type,
            object_id=object_id,
            parent=parent,
        )
