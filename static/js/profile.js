// 내 프로필 조회

const params = new URLSearchParams(location.search); // URL 파라미터 찾는 객체 만들어서
const userId = params.get('id'); 

const myProfile= async () => {
    try {
        const response = await axios.get(`user/profile/${userId}/`);  // API 요청
        const data = response.data;

        // html 파일에서 만든 form 에 데이터 채우기
        document.getElementById('nickname').textContent = data.nickname;
        document.getElementById('free-content').textContent = free.content;
        document.getElementById('live-content').textContent = live.content;
        document.getElementById('comments_count').textContent = data.comments_count;
        // 날짜도 백엔드에서 수정한 다음에 데이터 한번에 불러오면 좋겠다
        doucument.getElementById('created_at').textContent = new Date(data.created_at).toLocaleString();
        // 팔로잉, 팔로우, 북마크, 

        // 프로필 이미지 : null인 경우 처리작업 추가해야할거같다.. 일단 텍스트로
        const profileImage = free.author.profile_image ? `<img src="${free.author.profile_image}" alt="프로필 이미지" width="50">` : "이미지 없음";
        document.getElementById('free-profile-image').innerHTML = profileImage;

        // 소개글 : null 일때 어떻게?
        const intro = free.intro? free.intro : "빈 소개글입니다.";
        document.getElementById('free-intro').textContent = intro;
        
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