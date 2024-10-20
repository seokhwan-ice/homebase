from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, filters
from .models import ChatRoom, ChatMessage, ChatParticipant
from . import serializers
from user.serializers import UserSerializer


# 채팅방
class ChatRoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ChatRoom.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.ChatRoomCreateSerializer
        elif self.action == "list":
            return serializers.ChatRoomListSerializer
        elif self.action == "retrieve":
            return serializers.ChatRoomDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise PermissionDenied("방장만 삭제할 수 있습니다!")
        instance.delete()

    # 권한 설정
    def get_permissions(self):
        if self.action == "list":  # 목록 조회는 로그인 없이 가능
            permission_classes = [AllowAny]
        else:  # 채팅방 생성, 입장(상세조회)은 로그인 필수
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # 검색
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    # 채팅방에 참여하는 API (ChatParticipant 추가하기)
    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        room = self.get_object()
        participant, created = ChatParticipant.objects.get_or_create(
            user=request.user, room=room
        )
        user_serializer = UserSerializer(request.user)  # 사용자 정보 추가
        if created:
            return Response(
                {
                    "message": "참여 완료!",
                    "nickname": user_serializer.data["nickname"],
                },
                status=201,
            )
        return Response(
            {
                "message": "이미 참여 중입니다!",
                "nickname": user_serializer.data["nickname"],
            },
            status=200,
        )


# 채팅 메시지
# TODO: 페이지네이션 추가하기
class ChatMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChatMessageSerializer
    queryset = ChatMessage.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
