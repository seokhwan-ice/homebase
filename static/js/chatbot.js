// AI 챗봇 기능 처리
const socket = io.connect('https://home-base.co.kr');

// 메시지 전송 버튼 클릭 시 동작
document.getElementById('send-message-btn').addEventListener('click', () => {
    const userInput = document.getElementById('user-input').value;

    socket.emit('sendMessageToBot', { userInput });  // 서버로 메시지 전송
});

// 서버로부터 AI 챗봇의 응답 수신
socket.on('receiveBotMessage', (aiResponse) => {
    const chatBox = document.getElementById('chat-box');
    const botMessage = `<div>AI 챗봇: ${aiResponse}</div>`;  // 챗봇 응답 표시
    chatBox.innerHTML += botMessage;  // 응답을 대화창에 추가
});
