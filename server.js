// Socket.IO 서버 (3000포트에서 실행)
const io = require('socket.io')(3000, {
    cors: {
        origin: "*",  // 모든 도메인에서의 접근 허용 (CORS 문제 해결)
    }
});

// 메모리 내에 채팅방을 저장하는 객체(채팅방 ID 별로 메시지 저장함)
let chatRooms = {};
// TODO: 서버 종료되면 데이터 사라짐 >>> 장고 영구적 기록으로 변환해야됨

// 클라이언트가 연결되었을 때 이벤트 처리
io.on('connection', (socket) => {
    console.log('유저가 연결되었습니다!');

    // 클라이언트가 특정 채팅방 입장
    socket.on('joinRoom', ({ roomId, userNickname }) => {
        socket.join(roomId);  // 특정 roomId에 해당하는 채팅방에 사용자 입장
        console.log(`${userNickname} 님이 ${roomId} 방에 입장했습니다!!`);

        // 해당 채팅방이 없다면 생성
        if (!chatRooms[roomId]) {
            chatRooms[roomId] = [];
        }

        // 클라이언트에게 이전 채팅 내역을 전달
        socket.emit('previousMessages', chatRooms[roomId]);
    });

    // 클라이언트가 메시지를 보낼 때 처리
    socket.on('sendMessage', ({ roomId, userNickname, message }) => {
        const chatMessage = { userNickname, message, time: new Date().toLocaleTimeString() };

        // 해당 채팅방에 메시지를 저장
        chatRooms[roomId].push(chatMessage);

        // 채팅방에 있는 모든 클라이언트에게 메시지 전달
        io.to(roomId).emit('receiveMessage', chatMessage);
    });

    // 클라이언트 연결 해제 시
    socket.on('disconnect', () => {
        console.log('유저 연결이 해제되었습니다!');
    });
});