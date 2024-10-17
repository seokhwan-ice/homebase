// URL에서 쿼리 파라미터로부터 username 추출하기
const params = new URLSearchParams(window.location.search);
const username = params.get('username');  // URL에서 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 사용자 정보와 북마크한 글 가져오는 함수
const loadUserProfileAndBookmarks = async () => {
    try {
        // 서버로부터 사용자 정보와 북마크 목록 가져오기
        const response = await axios.get(`user/${username}/bookmark/`);
        const userData = response.data;

        // 프로필 이미지와 닉네임 설정
        document.getElementById('profile-image').src = userData.profile_image;
        document.getElementById('nickname').textContent = userData.nickname;

        // 북마크한 글의 제목 리스트 추가
        const bookmarksList = document.getElementById('bookmark-list');
        bookmarksList.innerHTML = ''; // 기존 리스트 초기화

        userData.bookmark.forEach(bookmark => {
            const listItem = document.createElement('li');

            // 게시글로 이동하는 링크 생성
            const link = document.createElement('a');

            // 게시물의 타입에 따라 다른 상세 페이지로 이동
            if (bookmark.article_type === "Free") {
                link.href = `free_detail.html?id=${bookmark.id}`;  // 자유게시판 글 상세페이지 링크
            } else if (bookmark.article_type === "Live") {
                link.href = `live_detail.html?id=${bookmark.id}`;  // 직관 게시판 글 상세페이지 링크
            }

            link.textContent = `${bookmark.article_type}: ${bookmark.title}`;  // 게시글 유형과 제목 표시

            // 북마크한 시간을 표시
            const timeSpan = document.createElement('span');
            timeSpan.textContent = `${bookmark.updated_at}`;  // 북마크한 시간 표시
            timeSpan.style.marginLeft = '10px';  // 시간과 제목 사이 간격 설정

            listItem.appendChild(link);
            listItem.appendChild(timeSpan);
            bookmarksList.appendChild(listItem);
        });

    } catch (error) {
        console.error("북마크 데이터를 불러오는 중 오류 발생:", error);
        alert('북마크 데이터를 불러오는 중 오류가 발생했습니다.');
    }
};

// 버튼 버튼 클릭 시 페이지 이동 설정
document.getElementById('community_posts-button').addEventListener('click', () => {
    window.location.href = `user_live_list.html?username=${username}`;
});
document.getElementById('free_posts-button').addEventListener('click', () => {
    window.location.href = `user_free_list.html?username=${username}`;
});
document.getElementById('comments-button').addEventListener('click', () => {
    window.location.href = `user_comment_list.html?username=${username}`;
});

// 페이지 로드 시 사용자 정보와 북마크된 글 불러옴
document.addEventListener('DOMContentLoaded', loadUserProfileAndBookmarks);
