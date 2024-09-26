from rest_framework import viewsets
from .models import Free
from .serializers import (
    FreeCreateUpdateSerializer,
    FreeListSerializer,
    FreeDetailSerializer,
)


class FreeViewSet(viewsets.ModelViewSet):
    queryset = Free.objects.all()  # 기본 쿼리셋

    # CRUD에 따른 시리얼라이저 반환
    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return FreeCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return FreeListSerializer  # Read:list
        elif self.action in ["retrieve", "destroy"]:
            return FreeDetailSerializer  # Read:detail, Delete

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # 작성자==현재유저

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True  # 일부만 수정하기 허용
        return super().update(request, *args, **kwargs)
