
// 자유게시판 글 등록 (free_create)

const form = document.getElementById('create-form');
// getElementById: 특정 ID 가진 HTML 요소를 가져오는 함수.
// 13번째 줄 id="create-form" form 태그에 데이터를 표시할거라는 뜻

form.addEventListener('submit', async function(event) {
    event.preventDefault();  // 기본 form 제출 방지 (페이지 새로고침 방지)

    if (!checkSignin()) return;

    const formData = new FormData(form);
    // FormData 객체 생성: JSON 말고 multipart/form-data 형식으로 서버 전송(이미지때문에)

    try {
        const response = await axios.post('community/free/', formData);
        const freeId = response.data.id;  // 생성된 글의 ID
        alert("글 등록 성공!");

        // // 브라우저 URL을 동적으로 변경
        // history.pushState(null, '', `/community/free/${freeId}`);
        location.href = `free_detail.html?id=${freeId}`;  // 상세 페이지로 이동

    } catch (error) {
        console.error("Error:", error);
        alert("글 등록 실패");
    }
});

// 이미지 미리보기
function previewImage(event) {
    const reader = new FileReader();
    const imageField = document.getElementById('image_preview');

    reader.onload = function() {
        imageField.src = reader.result;
        imageField.style.display = 'block';
    };

    if (event.target.files[0]) {
        reader.readAsDataURL(event.target.files[0]);
    }
}