// URL에서 쿼리 파라미터로부터 username 추출하기
const params = new URLSearchParams(window.location.search);
const username = params.get('username');  // URL에서 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 날짜 포맷팅 함수
const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('ko-KR', options);
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
        userData.comments.forEach(comment => {
            const listItem = document.createElement('li');

            // 댓글 내용과 댓글이 달린 게시물로의 링크
            const commentLink = document.createElement('a');
            commentLink.href = `/${comment.article_type.toLowerCase()}_article/${comment.article_id}`; // 해당 게시물로 이동
            commentLink.textContent = comment.content;

            // 최신 시간 계산 (생성 시간과 수정 시간 중 더 최신 시간)
            const createdAt = new Date(comment.created_at);
            const updatedAt = new Date(comment.updated_at);
            const latestTime = createdAt > updatedAt ? createdAt : updatedAt;

            // 시간 표시
            const timeElement = document.createElement('span');
            timeElement.textContent = ` (${formatDate(latestTime)})`;

            listItem.textContent = `[${comment.article_type}] `;
            listItem.appendChild(commentLink);
            listItem.appendChild(timeElement);  // 최신 시간 추가
            commentsList.appendChild(listItem);
        });

    } catch (error) {
        console.error("작성 댓글 데이터를 불러오는 중 오류 발생:", error);
        alert('작성 댓글 데이터를 불러오는 중 오류가 발생했습니다.');
    }
};

// 페이지 로드 시 사용자 정보와 작성 댓글을 불러옴
document.addEventListener('DOMContentLoaded', loadUserProfileAndComments);
