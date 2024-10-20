
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
            const defaultImage = '/static/images/baseball.png';  // 디폴트 이미지

            // chatroom_image
            const roomImage = room.image ? room.image.replace(/.*\/media/, '/media') : 'https://i.imgur.com/CcSWvhq.png';

            li.classList.add('chatroom-item');
            li.innerHTML = `
                <img src="${roomImage}" alt="채팅방 대표사진" class="chatroom-image">
                <div class="chatroom-info">
                    <h3 class="chatroom-title">${room.title}</h3>
                    <p class="chatroom-description">${room.description}</p>
                    <p class="chatroom-last-message">최근 대화: ${room.latest_message_time}</p>
                </div>
                <div class="chatroom-participants">
                    <i class="fa-solid fa-user"></i> ${room.participants_count}명
                </div>
            `;

            li.addEventListener('click', () => {
                window.location.href = `chatroom_detail.html?roomId=${room.id}`;
            });

            chatroomList.appendChild(li);
        });
    } catch (error) {
        console.error('채팅방 목록 불러오기 실패:', error);
    }
};

// DOMContentLoaded 이벤트에서 처음 목록 로드
document.addEventListener('DOMContentLoaded', async () => {
    await loadChatrooms();  // 전체 채팅방 목록 로드
});

// 검색 기능 추가
document.getElementById('search-button').addEventListener('click', async () => {
    const searchInput = document.getElementById('search-input').value;
    await loadChatrooms(searchInput);
});

// 채팅방 생성 버튼 클릭 시
document.getElementById('create-chatroom-button').addEventListener('click', () => {
    if (!checkSignin()) return;
    location.href = 'chatroom_create.html';
});