const axios = require('axios');  // Django API와 통신하기 위해 axios 사용

// 환경 변수를 기반으로 환경 설정
const environment = process.env.NODE_ENV || 'development';  // 'production' 또는 'development' 설정

// Socket.IO 서버 설정
const io = require('socket.io')(3000, {
    cors: {
        origin: environment === 'production'
            ? "http://home-base.co.kr"  // 배포 환경
            : ["http://localhost:8000", "http://127.0.0.1:5500"],  // 로컬 환경
        methods: ["GET", "POST"]
    }
});

// 클라이언트가 메시지를 보낼 때
io.on('connection', (socket) => {
    socket.on('chatbotUserMessage', async (messageData) => {
        const { userMessage, userNickname } = messageData;

        try {
            // Django API로 메시지 전송 (예시 URL로 교체)
            const response = await axios.post('http://localhost:8000/api/chatbot/conversations/', {
                user_input: userMessage,
            });

            // Django로부터 받은 응답
            const botResponse = response.data.ai_response;

            // 클라이언트에게 사용자 메시지와 챗봇 응답 전송
            io.emit('chatbotReceiveMessage', { userNickname, message: userMessage });
            io.emit('chatbotReceiveMessage', { userNickname: 'Chatbot', message: botResponse });
        } catch (error) {
            console.error('Django API 호출 중 오류 발생:', error);
        }
    });
});
