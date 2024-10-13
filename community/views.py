from django.db import models
from django.db.models import Q, F
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import viewsets, status, views
from .mixins import CommentMixin, BookmarkMixin, LikeMixin
from .models import Free, Live
from . import serializers
from chat.models import ChatRoom
from chat.serializers import ChatRoomSerializer


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

    def get_queryset(self):  # TODO: 인기기준에 대해서는 더 생각해보자 + 날짜고려
        queryset = super().get_queryset()
        sort = self.request.query_params.get("sort")
        if sort == "hot":
            queryset = queryset.annotate(
                hot=F("comments_count") * 3 + F("likes_count")
            ).order_by("-hot")
        return queryset


class MainView(views.APIView):
    def get(self, request):
        # community
        top_viewed_free = Free.objects.order_by("-views")[:3]
        top_commented_free = Free.objects.order_by("-comments_count")[:3]
        top_liked_live = Live.objects.order_by("-likes_count")[:3]
        top_commented_live = Live.objects.order_by("-comments_count")[:3]

        # data
        # latest_news = News.objects.order_by("-created_at")[:3]
        # top_commented_news = News.objects.order_by("-comments_count")[:3]
        # top_teams = Team.objects.order_by("-rank") # 팀순위는 전부 보여줘도 좋을 듯!
        # 또 더 보여주면 좋을만한거 생각해보자 선수순위? 그런것두 있나? 아니면 이번달 경기일정

        # chat
        top_participated_chatrooms = ChatRoom.objects.annotate(
            participants_count=models.Count("participants")
        ).order_by("-participants_count")[:3]

        top_data = {
            "top_viewed_free": serializers.FreeListSerializer(
                top_viewed_free, many=True
            ).data,
            "top_commented_free": serializers.FreeListSerializer(
                top_commented_free, many=True
            ).data,
            "top_liked_live": serializers.LiveListSerializer(
                top_liked_live, many=True
            ).data,
            "top_commented_live": serializers.LiveListSerializer(
                top_commented_live, many=True
            ).data,
            "top_participated_chatrooms": ChatRoomSerializer(
                top_participated_chatrooms, many=True
            ).data,
        }
        return Response(top_data, status=status.HTTP_200_OK)


# TODO: 여기에 data 앱 내용 추가해서 전체 메인페이지로 써도 좋을거 같애!
# TODO: 최신 뉴스 불러올려 했는데 News 모델이 없네요? 뉴스는 데이터베이스에 저장 안하나요?
# TODO: 팀 순위 불러올려 했는데 팀 순위 조회가 안되네요? 크롤링 해도 데이터베이스에 암것도 안들어오는데요?
