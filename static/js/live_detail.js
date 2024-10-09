
// 직관인증게시판 글 상세 (live_detail)

const params = new URLSearchParams(location.search);
const liveId = params.get('id');

// 댓글 목록 가져오기 함수
const getComments = (comments) => {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = '';  // 기존 댓글 초기화

    comments.forEach(comment => {
        const commentItem = document.createElement('div');
        commentItem.innerHTML = `
            <p>작성자: ${comment.author.nickname}</p>
            <p>댓글내용: ${comment.content}</p>
            <p>작성시간: ${new Date(comment.created_at).toLocaleString()}</p>
            <button class="reply-button" data-id="${comment.id}">답글</button><hr>
        `;
        commentsList.appendChild(commentItem);
    });
};

// 글 상세 (+ 댓글) 가져오기 함수
const getLiveDetail = async () => {
    try {
        const response = await axios.get(`community/live/${liveId}/`);
        const live = response.data;

        // html 파일에서 만든 form 에 데이터 채우기
        document.getElementById('game-info').textContent = `${live.home_team} vs ${live.away_team}`;
        document.getElementById('live-author').textContent = live.author.nickname;
        document.getElementById('live-seat').textContent = live.seat || "정보 없음";
        document.getElementById('live-stadium').textContent = live.stadium;
        document.getElementById('live-review').textContent = live.review;
        document.getElementById('live-likes-count').textContent = live.likes_count;
        document.getElementById('live-comments-count').textContent = live.comments_count;
        document.getElementById('live-created-at').textContent = new Date(live.created_at).toLocaleString();

        // 이미지 처리 >>> 백엔드에서 수정할게요 디폴트 이미지
        const profileImage = live.author.profile_image ? `<img src="${live.author.profile_image}" alt="프로필 이미지" width="50">` : "이미지 없음";
        document.getElementById('live-profile-image').innerHTML = profileImage;

        const liveImage = live.live_image ? `<img src="${live.live_image}" alt="게시글 이미지" width="100">` : "이미지 없음";
        document.getElementById('live-image').innerHTML = liveImage;

        // 댓글 목록 불러오기
        getComments(live.comments);

    } catch (error) {
        console.error("Error:", error);
        alert("글 상세 정보 불러오기 실패");
    }
};

getLiveDetail();


// 글 수정
document.getElementById('update-button').addEventListener('click', function() {

    if (!checkSignin()) return;

    location.href = `live_update.html?id=${liveId}`;
});

// 글 삭제
document.getElementById('delete-button').addEventListener('click', async function() {

    if (!checkSignin()) return;

    const confirmDelete = confirm('정말 삭제하시겠습니까?');
    if (confirmDelete) {
        try {
            await axios.delete(`community/live/${liveId}/`);
            alert('글이 삭제되었습니다!');
            location.href = 'live_list.html';
        } catch (error) {
            console.error('Error:', error);
            alert('글 삭제 실패');
        }
    }
});

// 댓글 등록
const commentForm = document.getElementById('comment-form');
commentForm.addEventListener('submit', async function(event) {
    event.preventDefault();

    if (!checkSignin()) return;

    const content = document.getElementById('comment-content').value;
    const formData = { content };

    try {
        const response = await axios.post(`community/live/${liveId}/create_comment/`, formData);
        alert('댓글 작성 성공!');

        getLiveDetail(); // 다시 불러오기 (방금 작성한 댓글 반영)
        document.getElementById('comment-content').value = '';  // 입력창 초기화

    } catch (error) {
        console.error("Error:", error);
        alert('댓글 작성 실패');
    }
});

// 북마트 토글
document.getElementById('bookmark-button').addEventListener('click', async function() {

    if (!checkSignin()) return;

    try {
        const response = await axios.post(`community/live/${liveId}/toggle_bookmark/`);
        // 나중에 아이콘으로 바꾸쟈
        if (response.status === 201) {
            alert('글이 북마크되었습니다!');
            document.getElementById('bookmark-button').textContent = '북마크 취소하기';
        } else if (response.status === 204) {
            alert('북마크가 취소되었습니다!');
            document.getElementById('bookmark-button').textContent = '북마크하기';
        }
    } catch (error) {
        console.error("Error:", error);
        alert('북마크 요청 실패');
    }
});

// 좋아요 토글
document.getElementById('like-button').addEventListener('click', async function() {

    if (!checkSignin()) return;

    try {
        const response = await axios.post(`community/live/${liveId}/toggle_like_article/`);
        // 나중에 아이콘으로 바꾸쟈
        if (response.status === 201) {
            alert('좋아요 성공!');
            document.getElementById('like-button').textContent = '좋아요 취소하기';
        } else if (response.status === 204) {
            alert('좋아요 취소!');
            document.getElementById('like-button').textContent = '좋아요 누르기';
        }
        getLiveDetail(); // 좋아요 수 업데이트 (방금 내가 누른 좋아요 반영)

    } catch (error) {
        console.error("Error:", error);
        alert('좋아요 요청 실패');
    }
});