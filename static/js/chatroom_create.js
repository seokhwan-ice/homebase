document.getElementById('chatroom-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const form = document.getElementById('chatroom-form');
    const formData = new FormData(form);

    try {
        const response = await axios.post('chat/chatrooms/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        alert('채팅방을 만들었습니다!');
        location.href = 'chatroom_list.html';
    } catch (error) {
        console.error('채팅방 생성 실패:', error);
        alert('채팅방 생성 실패');
    }
});

// 이미지 미리보기
document.getElementById('image').addEventListener('change', function(event) {
    const imagePreview = document.getElementById('preview-image');
    const previewText = document.querySelector('.upload-hint');  // 유도 멘트
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;  // 업로드한 이미지로 미리보기 변경
            previewText.style.display = 'none';  // 유도 멘트 숨김
        };
        reader.readAsDataURL(file);
    } else {
        // 파일 선택이 취소된 경우
        imagePreview.src = '/static/images/baseball.png';  // 디폴트 이미지로 변경
        previewText.style.display = 'block';  // 유도 멘트 다시 표시
    }
});
