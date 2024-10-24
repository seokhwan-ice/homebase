
const params = new URLSearchParams(location.search);
const freeId = params.get('id');

const getFreeDetailForUpdate = async () => {
    try {
        const response = await axios.get(`community/free/${freeId}/`);
        const free = response.data;

        document.getElementById('title').value = free.title;
        document.getElementById('content').value = free.content;

    } catch (error) {
        console.error("Error:", error);
    }
};

getFreeDetailForUpdate();

const form = document.getElementById('update-form');

form.addEventListener('submit', async function(event) {
    event.preventDefault();

    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;

    try {
        const response = await axios.put(`community/free/${freeId}/`, { title, content });
        alert('글 수정 완료!');

        // 브라우저 URL을 동적으로 변경
        // history.pushState(null, '', `/community/free/${freeId}`);
        location.href = `free_detail.html?id=${freeId}`;  // 상세 페이지로 이동

    } catch (error) {
        console.error("Error:", error);
        alert('글 수정 실패');
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