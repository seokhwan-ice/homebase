// 실시간 채팅 설정
document.addEventListener('DOMContentLoaded', async () => {
    const roomId = new URLSearchParams(window.location.search).get('roomId');
    let userNickname = '';  // 로그인된 사용자의 닉네임을 저장할 변수

    // 채팅방 참여자 등록 및 사용자 정보 가져오기
    try {
        // 참여자 등록
        const response = await axios.post(`chat/chatrooms/${roomId}/join/`);
        // 사용자 정보를 응답에서 가져옴
        userNickname = response.data.nickname; // 서버 응답에서 nickname 가져오기
        console.log('참여자 닉네임:', userNickname);  // 콘솔에서 닉네임 확인
    } catch (error) {
        console.error('참여자 등록 실패:', error);
        return;  // 실패하면 진행하지 않도록 종료
    }

    // Socket.IO 로직
    const socket = io('http://localhost:3000');

    // 채팅방 입장
    socket.emit('joinRoom', { roomId, userNickname });

    // 이전 메시지 로드
    socket.on('previousMessages', function(messages) {
        messages.forEach(message => addMessage(message));
    });

    // 메시지 전송
    document.getElementById('send-button').addEventListener('click', function() {
        const message = document.getElementById('chat-message-input').value;
        if (message.trim()) {  // 빈 메시지를 보내지 않도록 체크
            socket.emit('sendMessage', { roomId, userNickname, message });
            document.getElementById('chat-message-input').value = '';
        }
    });

    // 메시지 수신
    socket.on('receiveMessage', function(message) {
        addMessage(message);
    });
});

// 메시지를 추가하는 함수
function addMessage(message) {
    const li = document.createElement('li');
    li.textContent = `[${message.time}] ${message.userNickname}: ${message.message}`;
    document.getElementById('messages').appendChild(li);
}
