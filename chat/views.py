from django.shortcuts import render

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics
from .serializers import ChatRoomSerializer
from .models import ChatRoom


def test_page1(request):
    return render(request, "chat/test_page1.html")


def test_page2(request, room_name):
    return render(request, "chat/test_page2.html", {"room_name": room_name})


# List, Create
class ChatRoomListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # 생성은 로그인 유저만 가능
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    # # 정렬 필터
    # # /api/chat/chatrooms/?ordering=
    # # /api/chat/chatrooms/?ordering=
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = []

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)  # 방장 == 현재 요청한 유저


# Detail
class ChatRoomDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated] # 채팅방 입장은 로그인 유저만 가능
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    lookup_field = "id"  # URL에서 채팅방 id 사용하기
