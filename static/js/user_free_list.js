// URL에서 쿼리 파라미터로부터 username 추출하기
const params = new URLSearchParams(window.location.search);
const username = params.get('username');  // URL에서 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 사용자 정보와 작성 글 정보를 가져오는 함수
const loadUserProfileAndPosts = async () => {
    try {
        // 서버로부터 사용자 정보와 작성 글 목록 가져오기
        const response = await axios.get(`user/${username}/free/`);
        const userData = response.data;

        // 프로필 이미지와 닉네임 설정
        document.getElementById('profile-image').src = userData.profile_image;
        document.getElementById('nickname').textContent = userData.nickname;

        // 작성한 글의 제목 리스트 추가
        const postsList = document.getElementById('free-posts-list');
        userData.community_free_articles.forEach(article => {
            const listItem = document.createElement('li');
            const postLink = document.createElement('a');

            // 게시글 제목과 링크 설정
            postLink.textContent = article.title;  // 제목 표시
            postLink.href = `free_detail.html?id=${article.id}`;  // 게시글 ID로 상세 페이지 링크 설정
            
            // 이미지가 있는 경우 이미지 미리보기 추가
            if (article.free_image) {
                const imagePreview = document.createElement('img');
                imagePreview.src = article.free_image;
                imagePreview.alt = article.title;
                imagePreview.style.width = "50px";  // 이미지 크기 설정
                listItem.appendChild(imagePreview);
            }

            // 게시글 작성일 표시
            const dateInfo = document.createElement('span');
            dateInfo.textContent = ` (작성일: ${article.created_at})`;
            
            // 리스트 아이템 구성
            listItem.appendChild(postLink);
            listItem.appendChild(dateInfo);
            postsList.appendChild(listItem);
        });

    } catch (error) {
        console.error("작성 글 데이터를 불러오는 중 오류 발생:", error);
        alert('작성 글 데이터를 불러오는 중 오류가 발생했습니다.');
    }
};

// 버튼 클릭 시 페이지 이동 설정
document.getElementById('community_posts-button').addEventListener('click', () => {
    window.location.href = `user_live_list.html?username=${username}`;
});
document.getElementById('comments-button').addEventListener('click', () => {
    window.location.href = `user_comment_list.html?username=${username}`;
});
document.getElementById('saved_posts-button').addEventListener('click', () => {
    window.location.href = `user_bookmark_list.html?username=${username}`;
});

// 페이지 로드 시 사용자 정보와 작성 글 제목을 불러옴
document.addEventListener('DOMContentLoaded', loadUserProfileAndPosts);
