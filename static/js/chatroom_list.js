
// 채팅방 목록을 불러오는 함수
const loadChatrooms = async (searchQuery = '') => {
    const chatroomList = document.getElementById('chatroom-list');
    const roomsCount = document.getElementById('rooms-count');

    try {
        // 검색어가 있으면 search 쿼리로 요청
        const response = await axios.get(`chat/chatrooms/?search=${searchQuery}`);
        const rooms = response.data;

        // 목록 초기화 및 채팅방 개수 표시
        chatroomList.innerHTML = '';  // 기존 리스트 초기화
        roomsCount.textContent = searchQuery
            ? `검색결과: ${rooms.length}개의 채팅방이 검색되었습니다.`
            : `총 ${rooms.length}개의 채팅방이 있습니다.`;

        // 채팅방 목록 렌더링
        rooms.forEach(room => {
            const li = document.createElement('li');

            const roomImage = room.image ? room.image.replace(/.*\/media/, '/media') : 'https://i.imgur.com/CcSWvhq.png';
            const latestMessageTime = timeAgo(room.latest_message_time);

            li.classList.add('chatroom-item');
            li.innerHTML = `
                <img src="${roomImage}" alt="채팅방 대표사진" class="chatroom-image">
                <div class="chatroom-info">
                    <h3 class="chatroom-title">${room.title}</h3>
                    <p class="chatroom-description">${room.description}</p>
                    <p class="chatroom-last-message">최근대화 : ${latestMessageTime}</p>
                </div>
                <div class="chatroom-participants">
                    <i class="fa-solid fa-user"></i> ${room.participants_count}명
                </div>
            `;

            li.addEventListener('click', () => {
                if (!checkSignin()) return;
                location.href = `chatroom_detail.html?roomId=${room.id}`;
            });

            chatroomList.appendChild(li);
        });
    } catch (error) {
        console.error('채팅방 목록 불러오기 실패:', error);
    }
};

// 처음 목록 로드
document.addEventListener('DOMContentLoaded', async () => {
    await loadChatrooms();
});

// 검색
document.getElementById('search-button').addEventListener('click', async () => {
    const searchInput = document.getElementById('search-input').value;
    await loadChatrooms(searchInput);
});

// 검색 엔터
document.getElementById('search-input').addEventListener('keydown', async (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        await loadChatrooms(document.getElementById('search-input').value);
    }
});

// 채팅방 생성 버튼 클릭 시
document.getElementById('create-chatroom-button').addEventListener('click', () => {
    if (!checkSignin()) return;
    location.href = 'chatroom_create.html';
});

// 시간 계산 함수
function timeAgo(dateString) {
    const now = new Date();
    const past = new Date(dateString);
    const diffInMs = now - past;
    const diffInMinutes = Math.floor(diffInMs / 1000 / 60);

    if (diffInMinutes < 1) return '방금 전';
    if (diffInMinutes < 60) return `${diffInMinutes}분 전`;

    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) return `${diffInHours}시간 전`;

    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays < 7) return `${diffInDays}일 전`;

    // 7일 이상일 경우 >>> 날짜 표시
    return past.toLocaleDateString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit' });
}