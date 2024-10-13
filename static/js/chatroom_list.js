
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
            ? `검색 결과: ${rooms.length} 개의 채팅방이 있습니다.`
            : `총 채팅방: ${rooms.length} 개의 채팅방이 있습니다.`;

        // 채팅방 목록 렌더링
        rooms.forEach(room => {
            const li = document.createElement('li');
            const defaultImage = '../images/chatroom_default.jpg';  // 디폴트 이미지

            li.innerHTML = `
                <img src="${room.image || defaultImage}" alt="채팅방대표사진" class="chatroom-image">
                <h3>방제목: ${room.title}</h3>
                <p>방설명: ${room.description}</p>
                <p>참여인원: ${room.participants_count}명</p>
                <p>최근대화: ${room.latest_message_time}</p>
                <a href="chatroom_detail.html?roomId=${room.id}">채팅방 입장</a>
            `;
            chatroomList.appendChild(li);
        });
    } catch (error) {
        console.error('채팅방 목록 불러오기 실패:', error);
    }
};

// DOMContentLoaded 이벤트에서 처음 목록 로드
document.addEventListener('DOMContentLoaded', async () => {
    // 전체 채팅방 목록 로드
    await loadChatrooms();
});

// 검색 기능 추가
document.getElementById('search-button').addEventListener('click', async () => {
    const searchInput = document.getElementById('search-input').value;
    await loadChatrooms(searchInput);
});