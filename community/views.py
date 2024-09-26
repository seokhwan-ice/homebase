from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied  # 403_FORBIDDEN
from .models import Free, Live
from .serializers import (
    FreeCreateUpdateSerializer,
    FreeListSerializer,
    FreeDetailSerializer,
    LiveCreateUpdateSerializer,
    LiveListSerializer,
    LiveDetailSerializer,
)


class FreeViewSet(viewsets.ModelViewSet):
    queryset = Free.objects.all()

    # CRUD에 따른 시리얼라이저 반환
    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return FreeCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return FreeListSerializer  # Read:list
        elif self.action in ["retrieve", "destroy"]:
            return FreeDetailSerializer  # Read:detail, Delete

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # 작성자=현재유저

    def update(self, request, *args, **kwargs):
        free = self.get_object()
        if free.author != request.user:
            raise PermissionDenied("본인의 글만 수정할 수 있습니다!")
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("본인의 글만 삭제할 수 있습니다!")
        instance.delete()


class LiveViewSet(viewsets.ModelViewSet):
    queryset = Live.objects.all()

    # CRUD에 따른 시리얼라이저 반환
    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return LiveCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return LiveListSerializer  # Read:list
        elif self.action in ["retrieve", "destroy"]:
            return LiveDetailSerializer  # Read:detail, Delete

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # 작성자=현재유저

    def update(self, request, *args, **kwargs):
        live = self.get_object()
        if live.author != request.user:
            raise PermissionDenied("본인의 글만 수정할 수 있습니다!")
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("본인의 글만 삭제할 수 있습니다!")
        instance.delete()
