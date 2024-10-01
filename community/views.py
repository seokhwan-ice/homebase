from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import viewsets, status
from .mixins import CommentMixin, BookmarkMixin, LikeMixin
from .models import Free, Live
from . import serializers


# Free, Live 공통 로직
class BaseViewSet(viewsets.ModelViewSet, CommentMixin, BookmarkMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]  # TODO: 권한 논의 후 수정

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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

    def get_model(self):
        return Free

    # 키워드 검색
    def get_queryset(self):
        """
        URL경로 - /api/community/free/?q=keyword (GET)
        Params - {Key : Value} = {q : keyword}
        """
        queryset = Free.objects.all()
        search = self.request.query_params.get("q")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )  # TODO: 쿼리호출결과 확인해보고 감당안되면 제목만 검색하자요
        return queryset

    # 조회수 카운트
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LiveFilter(filters.FilterSet):
    """
    URL경로 - /api/community/live/?game_date=2024-10-01 (GET)
    URL경로 - /api/community/live/?team=kia_tigers (GET)
    URL경로 - /api/community/live/?stadium=잠실 (GET)

    Params {Key : Value} 여러 조건 동시에 필터링 가능해요
    날짜 - {game_date : 2024-10-01}
    팀 - {team : kia_tigers}
    경기장 - {stadium : 잠실}
    """

    game_date = filters.DateFilter(field_name="game_date", lookup_expr="date")
    stadium = filters.CharFilter(field_name="stadium")
    team = filters.CharFilter(method="filter_team")

    class Meta:
        model = Live
        fields = ["game_date", "stadium"]

    def filter_team(self, queryset, name, value):
        return queryset.filter(Q(home_team=value) | Q(away_team=value))


class LiveViewSet(BaseViewSet, LikeMixin):
    queryset = Live.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = LiveFilter

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return serializers.LiveCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return serializers.LiveListSerializer  # Read:list
        elif self.action in ["retrieve", "destroy"]:
            return serializers.LiveDetailSerializer  # Read:detail, Delete

    def get_model(self):
        return Live
