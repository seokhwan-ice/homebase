document.addEventListener('DOMContentLoaded', async () => {
    const chatroomList = document.getElementById('chatroom-list');

    try {
        const response = await axios.get('chat/chatrooms/');
        response.data.forEach(room => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="chatroom_detail.html?roomId=${room.id}">${room.title}</a>`;
            chatroomList.appendChild(li);
        });
    } catch (error) {
        console.error('채팅 목록 불러오기 실패:', error);
    }
});