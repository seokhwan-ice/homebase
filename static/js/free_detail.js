
// 자유게시판 글 상세 (free_detail)

const params = new URLSearchParams(location.search); // URL 파라미터 찾는 객체 만들어서
const freeId = params.get('id');  // id 파라미터 값 가져오기

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

    // 댓글 버튼에 대댓글 달기 버튼 추가하기 >> 후.. 왜 작동을 안하냐.. 수정해야됨
    document.querySelectorAll('.reply-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const parentId = event.target.getAttribute('data-id');
            document.getElementById('parent-id').value = parentId;  // parent_id 설정
            document.getElementById('comment-content').focus();  // 댓글폼 포커스
        });
    });
};


// 글 상세 (+ 댓글) 가져오기 함수
const getFreeDetail = async () => {
    try {
        const response = await axios.get(`community/free/${freeId}/`);
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

        // 댓글 목록 불러오기
        getComments(free.comments);

        // // 브라우저 URL 동적으로 변경
        // history.pushState(null, '', `/community/free/${freeId}`);

    } catch (error) {
        console.error("Error:", error);
        alert("글 상세 정보 불러오기 실패");
    }
};

getFreeDetail();


// 글 수정
document.getElementById('update-button').addEventListener('click', function() {
    if (!localStorage.getItem('token')) {
        alert('로그인이 필요합니다!');
        location.href = 'user.html';
        return;
    }
    location.href = `free_update.html?id=${freeId}`;  // 수정 페이지로 이동
});

// 글 삭제
document.getElementById('delete-button').addEventListener('click', async function() {
    if (!localStorage.getItem('token')) {
        alert('로그인이 필요합니다!');
        location.href = 'user.html';
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

// 댓글 등록
const commentForm = document.getElementById('comment-form');
commentForm.addEventListener('submit', async function(event) {
    event.preventDefault();

    if (!localStorage.getItem('token')) {
        alert('로그인이 필요합니다!');
        location.href = 'user.html';
        return;
    }

    const content = document.getElementById('comment-content').value;
    const formData = { content };

    // 대댓글인지 확인 : parent_id 값 가져오기  >>> 수정해야됨
    const parentId = document.getElementById('parent-id')?.value;
    if (parentId) {
        formData.parent_id = parentId;
    }

    try {
        const response = await axios.post(`community/free/${freeId}/create_comment/`, formData);
        alert('댓글 작성 성공!');

        getFreeDetail(); // 다시 불러오기 (방금 작성한 댓글 반영)

        // 입력창 초기화
        document.getElementById('comment-content').value = '';

    } catch (error) {
        console.error("Error:", error);
        alert('댓글 작성 실패');
    }
});

// 북마트 토글
document.getElementById('bookmark-button').addEventListener('click', async function() {
    if (!localStorage.getItem('token')) {
        alert('로그인이 필요합니다!');
        location.href = 'user.html';
        return;
    }

    try {
        const response = await axios.post(`community/free/${freeId}/toggle_bookmark/`);

        // 북마크 상태에 따라 버튼 텍스트 변경 >>> 나중에 아이콘으로 바꾸쟈
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