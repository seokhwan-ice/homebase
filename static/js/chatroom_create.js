document.getElementById('chatroom-form').addEventListener('submit', async (event) => {
    event.preventDefault();  // 기본 폼 제출 막기

    const form = document.getElementById('chatroom-form');
    const formData = new FormData(form);  // FormData로 폼 데이터 수집

    try {
        const response = await axios.post('chat/chatrooms/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',  // 파일 전송을 위해 설정
            },
        });

        alert('채팅방 만들기 성공!');
        location.href = 'chatroom_list.html';
    } catch (error) {
        console.error('채팅방 생성 실패:', error);
        alert('채팅방 생성 실패했습니다.');
    }
});