
// 자유게시판 글 수정 (free_update)

const params = new URLSearchParams(location.search); // URL 파라미터 찾는 객체 만들어서
const freeId = params.get('id');  // id 파라미터 값 가져오기

const getFreeDetailForUpdate = async () => {
    try {
        const response = await axios.get(`community/free/${freeId}/`);
        const free = response.data;  // 서버로부터 받은 데이터를 free 변수에 저장

        // html 파일에서 만든 form 에 데이터 채우기
        document.getElementById('title').value = free.title;
        document.getElementById('content').value = free.content;

    } catch (error) {
        console.error("Error:", error);
    }
};

getFreeDetailForUpdate();

const form = document.getElementById('update-form');

form.addEventListener('submit', async function(event) {
    event.preventDefault();  // 기본 form 제출 방지

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