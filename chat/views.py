from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import ChatRoom, ChatMessage, ChatParticipant
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from user.serializers import UserSerializer


# 채팅방
class ChatRoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

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
class ChatMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
