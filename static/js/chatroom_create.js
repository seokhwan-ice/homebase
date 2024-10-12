document.getElementById('create-chatroom-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const title = document.getElementById('chatroom-title').value;
    const description = document.getElementById('chatroom-description').value;

    try {
        await axios.post('chat/chatrooms/', { title, description });
        alert('채팅방 만들기 성공!');
        location.href = 'chatroom_list.html';
    } catch (error) {
        console.error('채팅방 만들기 실패:', error);
    }
});