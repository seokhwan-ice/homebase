// URL에서 쿼리 파라미터로부터 username 추출하기
const params = new URLSearchParams(window.location.search);
const username = params.get('username');  // URL에서 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 사용자 정보와 작성 댓글 목록을 가져오는 함수
const loadUserProfileAndComments = async () => {
    try {
        // 서버로부터 사용자 정보와 작성 댓글 목록 가져오기
        const response = await axios.get(`user/${username}/commentlist/`);
        const userData = response.data;

        // 프로필 이미지와 닉네임 설정
        document.getElementById('profile-image').src = userData.profile_image;
        document.getElementById('nickname').textContent = userData.nickname;

        // 작성한 댓글 리스트 추가
        const commentsList = document.getElementById('comment-list');
        commentsList.innerHTML = '';  // 기존 리스트 초기화

        userData.comments.forEach(comment => {
            const listItem = document.createElement('li');

            // 댓글이 달린 게시물로의 링크 생성 (Free 또는 Live에 따라)
            const commentLink = document.createElement('a');
            if (comment.article_type === "Free") {
                commentLink.href = `free_detail.html?id=${comment.id}`; // 자유게시판 상세페이지로 이동
            } else if (comment.article_type === "Live") {
                commentLink.href = `live_detail.html?id=${comment.id}`; // 직관 게시판 상세페이지로 이동
            }

            commentLink.textContent = `${comment.article_type}: ${comment.content}`;  // 게시글 유형과 댓글 내용 표시

            // 댓글 작성 또는 수정 시간을 표시
            const timeSpan = document.createElement('span');
            timeSpan.textContent = `${comment.updated_at}`;  // 최신 수정 시간 표시
            timeSpan.style.marginLeft = '10px';  // 시간과 댓글 내용 사이 간격 설정

            listItem.appendChild(commentLink);
            listItem.appendChild(timeSpan);
            commentsList.appendChild(listItem);
        });

    } catch (error) {
        console.error("작성 댓글 데이터를 불러오는 중 오류 발생:", error);
        alert('작성 댓글 데이터를 불러오는 중 오류가 발생했습니다.');
    }
};

// mypage 버튼 클릭 시 페이지 이동 설정
document.getElementById('mypage-button').addEventListener('click', () => {
    window.location.href = `user_main_profile.html?username=${username}`;
});

// 버튼 버튼 클릭 시 페이지 이동 설정
document.getElementById('community_posts-button').addEventListener('click', () => {
    window.location.href = `user_live_list.html?username=${username}`;
});
document.getElementById('free_posts-button').addEventListener('click', () => {
    window.location.href = `user_free_list.html?username=${username}`;
});
document.getElementById('saved_posts-button').addEventListener('click', () => {
    window.location.href = `user_bookmark_list.html?username=${username}`;
});

// sign-out버튼
document.getElementById('signout-button').addEventListener('click', () => {
    // 로그아웃 후 메인 페이지로 리디렉션
    localStorage.removeItem('access_token');  // 토큰 제거
    localStorage.removeItem('refresh_token');
    alert('로그아웃 완료!');
    window.location.href = '/';  // 로그아웃 후 메인 페이지로 이동
});

// sign-out버튼
document.getElementById('signout-button').addEventListener('click', () => {
    // 로그아웃 후 메인 페이지로 리디렉션
    localStorage.removeItem('access_token');  // 토큰 제거
    localStorage.removeItem('refresh_token');
    alert('로그아웃 완료!');
    window.location.href = '/';  // 로그아웃 후 메인 페이지로 이동
});

// 페이지 로드 시 사용자 정보와 작성 댓글을 불러옴
document.addEventListener('DOMContentLoaded', loadUserProfileAndComments);
