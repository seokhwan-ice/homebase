from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

# 요약
# ws/chat/<room_name>/ 경로로 들어오면, ChatConsumer가 그 요청을 처리하도록 연결 설정

# re_path
# (regular 약자인가봐) 정규표현식을 사용해서 URL 패턴을 정의하는 함수

# ws/chat/
# ws/chat/로 시작하는 경로에 대해 Websocket 연결 설정한다는 뜻

# (?P<room_name>\w+)
# 이부분이 정규 표현식!!
# \w+ 는 그냥 영문자, 숫자, 밑줄로 이루어진 문자열이라는 뜻! (복잡한거 아님)
# room_name 을 URL에서 추출해서 채팅방 이름으로 전달함
# ex) ws/chat/homebase/ -> homebase 채팅방

# consumers.ChatConsumer.as_asgi()
# consumers.py 에서 정의한 소비자(ChatConsumer)가 ASGI 형식으로 요청을 처리하도록 설정
