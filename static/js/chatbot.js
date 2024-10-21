document.addEventListener('DOMContentLoaded', () => {
    // Socket.IO 서버에 연결 설정 (포트는 서버에 맞게 수정)
    const socket = io('http://localhost:3000');  // 로컬 서버에 연결 (배포 시 URL 변경)

    // 이전 메시지 불러오기
    socket.on('chatbotPreviousMessages', (messages) => {
        messages.forEach((message) => {
            addMessageToChatbot(message);
        });
    });

    // 메시지 전송 버튼 클릭 이벤트
    document.getElementById('chatbot-send-button').addEventListener('click', () => {
        const messageInput = document.getElementById('chatbot-message-input');
        const message = messageInput.value.trim();
        const userNickname = '사용자';  // 사용자의 닉네임 (여기서는 간단히 설정)

        if (message !== '') {
            socket.emit('chatbotUserMessage', { userMessage: message, userNickname });
            messageInput.value = '';  // 메시지 전송 후 입력 필드 비우기
        }
    });

    // 서버로부터 메시지 수신
    socket.on('chatbotReceiveMessage', (messageData) => {
        addMessageToChatbot(messageData);  // 받은 메시지를 화면에 표시
    });

    // 메시지를 챗봇 UI에 추가하는 함수
    function addMessageToChatbot(messageData) {
        const messageContainer = document.getElementById('chatbot-messages');
        const messageElement = document.createElement('div');
        messageElement.classList.add('chatbot-message');
        messageElement.innerHTML = `<strong>${messageData.userNickname}:</strong> ${messageData.message}`;
        messageContainer.appendChild(messageElement);

        // 채팅 창 스크롤을 맨 아래로 내리기
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }
});
