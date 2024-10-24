// URL에서 쿼리 파라미터로부터 username 추출하기
const params = new URLSearchParams(window.location.search);
const username = params.get('username');  // URL에서 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 사용자 정보와 커뮤니티 작성 글 가져오는 함수
const loadUserProfileAndLivePosts = async () => {
    try {
        // 서버로부터 사용자 정보와 작성한 live 게시글 목록 가져오기
        const response = await axios.get(`user/${username}/live/`);
        const userData = response.data;

        // 프로필 이미지와 닉네임 설정
        document.getElementById('profile-image').src = userData.profile_image;
        document.getElementById('nickname').textContent = userData.nickname;

        // 작성한 live 게시글 리스트 추가
        const livePostsList = document.getElementById('live-posts-list');
        userData.community_live_articles.forEach((article) => {
            const listItem = document.createElement('li');

            // 게시글 이미지와 링크 생성
            const link = document.createElement('a');
            link.href = `live_detail.html?id=${article.id}`;  // 게시글 상세 페이지로 이동하는 링크

            // 이미지 추가
            if (article.live_image) {
                const img = document.createElement('img');
                img.src = article.live_image;
                img.width = 100;  // 이미지 너비 설정
                img.alt = "Live Image";  // 이미지 대체 텍스트
                link.appendChild(img);  // 링크 안에 이미지 추가
            }

            // 날짜 정보 추가
            const timeSpan = document.createElement('span');
            timeSpan.textContent = ` (작성일 ${article.created_at})`;
            timeSpan.style.marginLeft = '10px';  // 시간과 이미지 간격 설정

            listItem.appendChild(link);  // 이미지(링크) 추가
            listItem.appendChild(timeSpan);  // 날짜 추가
            livePostsList.appendChild(listItem);
        });

    } catch (error) {
        console.error("작성 글 데이터를 불러오는 중 오류 발생:", error);
        alert('작성 글 데이터를 불러오는 중 오류가 발생했습니다.');
    }
};

// 버튼 클릭 시 페이지 이동 설정
document.getElementById('free_posts-button').addEventListener('click', () => {
    window.location.href = `user_free_list.html?username=${username}`;
});
document.getElementById('comments-button').addEventListener('click', () => {
    window.location.href = `user_comment_list.html?username=${username}`;
});
document.getElementById('saved_posts-button').addEventListener('click', () => {
    window.location.href = `user_bookmark_list.html?username=${username}`;
});

// 페이지 로드 시 사용자 정보와 작성한 커뮤니티 글 목록을 불러옴
document.addEventListener('DOMContentLoaded', loadUserProfileAndLivePosts);
