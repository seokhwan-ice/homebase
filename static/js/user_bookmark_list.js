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
        userData.bookmark.forEach(bookmark => {
            const listItem = document.createElement('li');

            // 게시글로 이동하는 링크 생성
            const link = document.createElement('a');
            link.href = `/articles/${bookmark.article_type}/${bookmark.title}`;  // 해당 게시글로 이동하는 링크
            link.textContent = `${bookmark.article_type}: ${bookmark.title}`;  // 게시글 유형과 제목 표시

            // 북마크한 시간을 표시
            const timeSpan = document.createElement('span');
            timeSpan.textContent = ` | ${bookmark.updated_at}`;  // 북마크한 시간 표시
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

// 페이지 로드 시 사용자 정보와 북마크된 글 불러옴
document.addEventListener('DOMContentLoaded', loadUserProfileAndBookmarks);

//>>>>>>>>>>>> 직관 인증글의 데이터가 있을때 문제