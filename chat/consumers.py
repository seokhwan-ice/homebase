import json
from channels.generic.websocket import AsyncWebsocketConsumer


# Websocket 소비자: 연결을 수락, 메시지를 수신 및 전송하는 역할
class ChatConsumer(AsyncWebsocketConsumer):

    # Websocket 연결을 수락
    async def connect(self):
        # scope: URL 파라미터에서 room_name(채팅방 이름) 가져오기
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # chat_ 으로 시작하는 방 만들기 ex) chat_homebase
        self.room_group_name = f"chat_{self.room_name}"

        # 그룹 참가
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # Websocket 연결 허용
        await self.accept()

    # Websocket 연결 종료
    # close_code: 연결이 끊긴 이유나 상태 코드 <- 추가
    async def disconnect(self, close_code):
        # 그룹 나가기
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Websocket으로부터 메시지 받기
    async def receive(self, text_data):

        # text_data: 메시지(문자열)
        text_data_json = json.loads(text_data)
        # text_data_json: json 형식으로 받은 데이터에서 "메시지" 추출
        message = text_data_json["message"]

        # 그룹채팅방에 메시지 보내기
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # 그룹채팅방에서 메시지 받기
    async def chat_message(self, event):
        message = event["message"]

        # Websocket으로 메시지 전송
        await self.send(text_data=json.dumps({"message": message}))
