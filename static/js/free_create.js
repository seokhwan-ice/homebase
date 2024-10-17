
const form = document.getElementById('create-form');

form.addEventListener('submit', async function(event) {
    event.preventDefault();

    if (!checkSignin()) return;

    const formData = new FormData(form);

    try {
        const response = await axios.post('community/free/', formData);
        const freeId = response.data.id;
        alert("글 등록 성공!");

        // // 브라우저 URL을 동적으로 변경
        // history.pushState(null, '', `/community/free/${freeId}`);
        location.href = `free_detail.html?id=${freeId}`;

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