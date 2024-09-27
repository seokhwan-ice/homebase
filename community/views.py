from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied  # 403_FORBIDDEN
from .models import Free, Live
from . import serializers


# Free, Live 에서 공통된 로직
class CommunityViewSet(viewsets.ModelViewSet):

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


class FreeViewSet(CommunityViewSet):
    queryset = Free.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return serializers.FreeCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return serializers.FreeListSerializer  # Read:list
        elif self.action in ["retrieve", "destroy"]:
            return serializers.FreeDetailSerializer  # Read:detail, Delete


class LiveViewSet(CommunityViewSet):
    queryset = Live.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return serializers.LiveCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return serializers.LiveListSerializer  # Read:list
        elif self.action in ["retrieve", "destroy"]:
            return serializers.LiveDetailSerializer  # Read:detail, Delete
