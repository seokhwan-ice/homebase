document.addEventListener('DOMContentLoaded', async () => {
    const roomId = new URLSearchParams(location.search).get('roomId');
    let userNickname = '';
    let userProfileImage = '';

    // 채팅방 정보
    try {
        const response = await axios.get(`chat/chatrooms/${roomId}/`);
        const chatroom = response.data;

        // chatroom_image
        const chatroomImage = chatroom.image
            ? chatroom.image.replace(/.*\/media/, '/media')
            : 'https://i.imgur.com/CcSWvhq.png';

        document.getElementById('chatroom-image').src = chatroomImage;
        document.getElementById('chatroom-title').textContent = chatroom.title
        document.getElementById('chatroom-description').textContent = chatroom.description
        document.getElementById('participants-count').textContent = chatroom.participants_count || '0';

        // 현재 유저 === 방장 >>>>> 방 삭제 버튼 표시
        const userId = response.data.user_id;

        if (chatroom.creator_id === userId) {
            document.getElementById('delete-chatroom-button').style.display = 'block';
        }

    } catch (error) {
        alert('채팅방 정보 불러오기 실패..');
        return;
    }

    // 참여자 등록
    try {
        const response = await axios.post(`chat/chatrooms/${roomId}/join/`);
        userNickname = response.data.nickname;
        userProfileImage = response.data.profile_image;

        // 참여자 수 바로 업데이트
        const roomResponse = await axios.get(`chat/chatrooms/${roomId}/`);
        const participantsCount = roomResponse.data.participants_count;
        document.getElementById('participants-count').textContent = participantsCount;

    } catch (error) {
        return;
    }

    // Socket.IO 연결
    let socket;
    if (location.hostname === 'home-base.co.kr') {
        socket = io('https://home-base.co.kr', { transports: ['websocket', 'polling'], secure: true });
    } else {
        socket = io('http://127.0.0.1:3000');
    }

    // 채팅방 입장
    socket.emit('joinRoom', { roomId, userNickname });

    // 이전 메시지 로드
    socket.on('previousMessages', function(messages) {
        messages.forEach(message => addMessage(message));
    });

    // 메시지 입력 엔터키 >>> MAC 엔터 이슈
    let isComposing = false;
    document.getElementById('chat-message-input').addEventListener('compositionstart', () => {
        isComposing = true;
    });
    document.getElementById('chat-message-input').addEventListener('compositionend', () => {
        isComposing = false;
    });
    document.getElementById('chat-message-input').addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !isComposing) {
            event.preventDefault();
            document.getElementById('send-button').click();
        }
    });

    // 메시지 전송
    document.getElementById('send-button').addEventListener('click', async function() {
        const message = document.getElementById('chat-message-input').value;
        if (message.trim()) {  // 빈 메시지 안보내도록 체크

            // 1. Socket.IO로 메시지 전송
            socket.emit('sendMessage', {
                roomId,
                userNickname,
                message,
                user_profile_image: userProfileImage
            });

            // 2. 서버에 메시지 저장
            try {
                const response = await axios.post('chat/messages/', {
                    room: roomId,
                    content: message
                });
            } catch (error) {
            }

            // 3. 입력 필드 비우기
            document.getElementById('chat-message-input').value = '';
        }
    });

    // 메시지 수신
    socket.on('receiveMessage', function(message) {
        addMessage(message);
    });

    // 채팅방 삭제
    document.getElementById('delete-chatroom-button').addEventListener('click', async function() {
        if (confirm('이 채팅방을 정말 삭제하시나요????')) {
            try {
                await axios.delete(`chat/chatrooms/${roomId}/`);
                alert('채팅방 삭제 완료!');
                location.href = 'chatroom_list.html';
            } catch (error) {
                alert('채팅방 삭제 실패.');
            }
        }
    });

    // 채팅방 나가기
    document.getElementById('leave-chatroom-button').addEventListener('click', async function() {
        if (confirm('이 채팅방에서 나가시나요???')) {
            try {
                const roomId = new URLSearchParams(location.search).get('roomId');
                await axios.post(`chat/chatrooms/${roomId}/leave/`);
                alert('채팅방에서 나갔습니다!');
                location.href = 'chatroom_list.html';
            } catch (error) {
                alert('채팅방 나가기 실패.');
            }
        }
    });
});

// 메시지를 추가하는 함수
function addMessage(message) {

    // profile_image
    const userProfileImage = message.user_profile_image
        ? message.user_profile_image.replace(/.*\/media/, '/media')
        : 'https://i.imgur.com/CcSWvhq.png';

    const li = document.createElement('li');
    li.classList.add('message-item');
    li.innerHTML = `
        <img src="${userProfileImage}" alt="프사" class="message-profile-image">
        <div class="message-content">
            <span class="message-nickname">${message.userNickname}</span>
            <p class="message-text">${message.message}</p>
        </div>
        <span class="message-time">${message.time}</span>
    `;
    document.getElementById('messages').appendChild(li);

    // 스크롤 맨 아래로
    const chatWindow = document.querySelector('.chat-window');
    chatWindow.scrollTop = chatWindow.scrollHeight;
}