
// // 자유게시판 글 상세 (free_detail)

const params = new URLSearchParams(location.search); // URL 파라미터 찾는 객체 만들어서
const freeId = params.get('id');  // id 파라미터 값 가져오기

const getFreeDetail = async () => {
    try {
        const response = await axios.get(`community/free/${freeId}/`);  // API 요청
        const free = response.data;

        // html 파일에서 만든 form 에 데이터 채우기
        document.getElementById('free-title').textContent = free.title;
        document.getElementById('free-author').textContent = free.author.nickname;
        document.getElementById('free-content').textContent = free.content;
        document.getElementById('free-views').textContent = free.views;
        document.getElementById('free-comments-count').textContent = free.comments_count;
        // 날짜도 백엔드에서 수정한 다음에 데이터 한번에 불러오면 좋겠다
        document.getElementById('free-created-at').textContent = new Date(free.created_at).toLocaleString();
        document.getElementById('free-updated-at').textContent = new Date(free.updated_at).toLocaleString();

        // 프로필 이미지 : null인 경우 처리작업 추가해야할거같다.. 일단 텍스트로
        const profileImage = free.author.profile_image ? `<img src="${free.author.profile_image}" alt="프로필 이미지" width="50">` : "이미지 없음";
        document.getElementById('free-profile-image').innerHTML = profileImage;

        // 게시글 이미지 : null인 경우 처리작업 추가해야할거같다.. 일단 텍스트로
        const freeImage = free.free_image ? `<img src="${free.free_image}" alt="게시글 이미지" width="100">` : "이미지 없음";
        document.getElementById('free-image').innerHTML = freeImage;

        // // 브라우저 URL 동적으로 변경
        // history.pushState(null, '', `/community/free/${freeId}`);

    } catch (error) {
        console.error("Error:", error);
    }
};

getFreeDetail();

// 수정 버튼
document.getElementById('update-button').addEventListener('click', function() {

    const token = localStorage.getItem('token');
    if (!token) {
        alert('로그인이 필요합니다!');
        location.href = 'user.html';  // 로그인창으로 이동
        return;
    }

    location.href = `free_update.html?id=${freeId}`  // 수정 페이지로 이동
});

// 삭제 버튼
document.getElementById('delete-button').addEventListener('click', async function() {

    const token = localStorage.getItem('token');
    if (!token) {
        alert('로그인이 필요합니다!');
        location.href = 'user.html';  // 로그인창으로 이동
        return;
    }

    const confirmDelete = confirm('정말 삭제하시겠습니까?????');
    if (confirmDelete) {
        try {
            await axios.delete(`community/free/${freeId}/`);
            alert('글이 삭제되었습니다!');
            location.href = 'free_list.html';  // 삭제 후 목록 페이지로 이동
        } catch (error) {
            console.error('Error:', error);
            alert('글 삭제 실패');
        }
    }
});
