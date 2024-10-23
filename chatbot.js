const axios = require('axios');

const environment = process.env.NODE_ENV || 'production';

const io = require('socket.io')(3001, {
    cors: {
        origin: environment === 'production'
            ? "https://home-base.co.kr"
            : ["http://localhost:8000", "http://127.0.0.1:8000","http://127.0.0.1:5500"],
        methods: ["GET", "POST"],
        credentials: true,
        secure: true,
        // allowedHeaders: ["Content-Type", "Authorization"]
    }
});

const chatbotNamespace = io.of('/chatbot');
chatbotNamespace.on('connection', (socket) => {
    console.log("Chatbot namespace에 클라이언트가 연결되었습니다.");

    socket.on('chatbotUserMessage', async (messageData) => {
        const { userMessage, userNickname } = messageData;

        try {
            const response = await axios.post('https://home-base.co.kr/api/chatbot/conversations/', {
                user_input: userMessage,
            });

            const botResponse = response.data.ai_response;
            console.log(botResponse);

            socket.emit('chatbotReceiveMessage', { userNickname, message: userMessage });
            socket.emit('chatbotReceiveMessage', { userNickname: 'Chatbot', message: botResponse });
        } catch (error) {
            console.error('Django API 호출 중 오류 발생:', error);
        }
    });
});
