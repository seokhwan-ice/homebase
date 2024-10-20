// Socket.IO 서버 (3000포트에서 실행)

const environment = process.env.NODE_ENV || 'production';

const io = require('socket.io')(3000, {
    cors: {
        origin: environment === 'production'
            ? "http://home-base.co.kr"  // 배포 환경
            : "*",  // 로컬 환경 >>> 나 아직 쓸거라서 남겨둘게요
        methods: ["GET", "POST"]
    }
});

// 메모리 내에 채팅방을 저장하는 객체(채팅방 ID 별로 메시지 저장함)
let chatRooms = {};
// TODO: 서버 종료되면 데이터 사라짐 >>> 장고 영구적 기록으로 변환해야됨

// 클라이언트가 연결되었을 때 이벤트 처리
io.on('connection', (socket) => {
    console.log('유저가 연결되었습니다!');

    // 채팅방 입장
    socket.on('joinRoom', ({ roomId, userNickname }) => {
        socket.join(roomId);  // 특정 roomId에 해당하는 채팅방에 사용자 입장
        console.log(`${userNickname} >>> ${roomId} 방에 입장했습니다!!`);

        // 해당 채팅방이 없다면 생성
        if (!chatRooms[roomId]) {
            chatRooms[roomId] = [];
            console.log(`새로운 채팅방 생성됨: ${roomId}`);
        }

        // 클라이언트에게 이전 채팅 내역을 전달
        socket.emit('previousMessages', chatRooms[roomId]);
        console.log(`이전 메시지 전달 완료: ${chatRooms[roomId].length}개 메시지`);
    });

    // 클라이언트가 메시지를 보낼 때 처리
    socket.on('sendMessage', ({ roomId, userNickname, message, user_profile_image }) => {
        console.log('받은 메시지:', { roomId, userNickname, message, user_profile_image });

        const chatMessage = {
            userNickname,
            message,
            time: new Date().toLocaleTimeString(),
            user_profile_image
        };

        // 해당 채팅방에 메시지를 저장
        chatRooms[roomId].push(chatMessage);
        console.log(`메시지 저장 완료: ${message}`);

        // 채팅방에 있는 모든 클라이언트에게 메시지 전달
        io.to(roomId).emit('receiveMessage', chatMessage);
        console.log(`메시지 전송 완료: ${message}`);
    });

    // 방 나갈때
    socket.on('leaveRoom', ({ roomId, userNickname }) => {
        socket.leave(roomId);
        console.log(`${userNickname} >>> ${roomId} 방에서 나갔습니다.`);
    });
});