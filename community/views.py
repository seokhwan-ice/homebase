from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Free, Live, Comment, Like, Bookmark
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
                return NotFound("해당 부모 댓글을 찾을 수 없음")

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

    @action(detail=True, methods=["put"])  # TODO: PATCH로 수정할지 물어보기
    def update_comment(self, request, pk=None):
        instance = self.get_object()
        comment = self.get_comment(request, instance)
        serializer = serializers.CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def delete_comment(self, request, pk=None):
        instance = self.get_object()
        comment = self.get_comment(request, instance)
        comment.delete()
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
            return Response(
                data={"detail": "좋아요 취소됨"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(data={"detail": "좋아요!"}, status=status.HTTP_201_CREATED)

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


# Free, Live 공통 로직
class BaseViewSet(viewsets.ModelViewSet, CommentMixin, BookmarkMixin):
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


# 팔로우
