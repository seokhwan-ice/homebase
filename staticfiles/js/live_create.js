
// 직관인증게시판 글 등록 (live_create)

const form = document.getElementById('create-form');
form.addEventListener('submit', async function(event) {
    event.preventDefault();

    if (!checkSignin()) return;

    const formData = new FormData(form);  // 이미지 포함 전송하기 위함
    try {
        const response = await axios.post('community/live/', formData);
        const liveId = response.data.id;
        alert("Live 글 등록 성공!");
        location.href = `live_detail.html?id=${liveId}`;  // 상세 페이지 이동
    } catch (error) {
        console.error("Error:", error);
        alert("글 등록 실패");
    }
});