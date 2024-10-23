
const params = new URLSearchParams(location.search);
const liveId = params.get('id');

// 댓글 목록 가져오기 함수
const getComments = (comments) => {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = '';  // 기존 댓글 초기화

    comments.forEach(comment => {
        const commentItem = createCommentItem(comment);  // 댓글 생성 함수 호출
        commentsList.appendChild(commentItem);

        // 대댓글 표시
        if (comment.replies) {
            getReplies(comment.replies, comment.id);  // 대댓글 목록 가져오기 함수 호출
        }
    });

    addReplyEvents();  // 대댓글 작성 이벤트 추가
    addUpdateEvents();  // 댓글 수정 이벤트 추가
    addDeleteEvents();  // 댓글 삭제 이벤트 추가
    addLikeEvents();  // 댓글 좋아요 이벤트 추가
};

// 대댓글 목록 가져오기 함수
const getReplies = (replies, parentId) => {
    const replyList = document.getElementById(`reply-list-${parentId}`);
    replies.forEach(reply => {
        const replyItem = createCommentItem(reply);  // 대댓글 생성 함수 호출
        replyList.appendChild(replyItem);

        if (reply.replies && reply.replies.length > 0) {
            getReplies(reply.replies, reply.id); // 재귀적으로 대대댓글 처리
        }
    });
};

// 댓글 아이템 생성 함수
const createCommentItem = (comment) => {
    const commentItem = document.createElement('div');
    commentItem.classList.add('comment-item');

    // 작성자의 프로필 이미지
    const commentProfileImage = comment.author.profile_image
        ? comment.author.profile_image.replace(/.*\/media/, '/media')
        : 'https://i.imgur.com/CcSWvhq.png';  // 기본 이미지

    const isAuthor = comment.author.username === localStorage.getItem('username'); // 작성자인지 여부 확인
    const buttons = isAuthor ? `
        <button class="reply-button" data-id="${comment.id}">답글</button>
        <button class="update-button" data-id="${comment.id}">수정</button>
        <button class="delete-button" data-id="${comment.id}">삭제</button>
    ` : `
        <button class="reply-button" data-id="${comment.id}">답글</button>
    `;

    const likeCount = comment.likes_count || 0;

    commentItem.innerHTML = `
        <div class="comment-header">
            <div class="comment-author-info">
                <img class="comment-profile-image" src="${commentProfileImage}" alt="프로필 이미지">
                <span class="comment-author">${comment.author.nickname}</span>
            </div>
            <span class="comment-time">${new Date(comment.created_at).toLocaleString()}</span>
        </div>
        <div class="comment-body">
            <div class="comment-content">${comment.content}</div>
            <div class="comment-buttons">
                ${buttons}
                <button class="like-comment-button" data-id="${comment.id}">
                    <i class="fa fa-heart"></i> <span class="like-count">${likeCount}</span> <!-- 하트 아이콘과 좋아요 수 표시 -->
                </button>
            </div>
        </div>
        <hr class="comment-hr">
        <div class="reply-list" id="reply-list-${comment.id}"></div>
    `;
    return commentItem;
};

// 댓글 작성 이벤트 추가 함수
const addReplyEvents = () => {
    document.querySelectorAll('.reply-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const parentId = event.target.getAttribute('data-id');
            const replyForm = createReplyForm(parentId);  // 대댓글 작성 폼 생성
            document.getElementById(`reply-list-${parentId}`).appendChild(replyForm);
        });
    });
};

// 댓글 수정 이벤트 추가 함수
const addUpdateEvents = () => {
    document.querySelectorAll('.update-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const commentId = event.target.getAttribute('data-id');
            const commentItem = event.target.closest('.comment-item');

            const existingForm = commentItem.querySelector('.update-form');
            if (existingForm) {
                alert("이미 수정 폼이 열려 있어요!");
                return;
            }

            const currentContent = commentItem.querySelector('.comment-content').textContent;
            const updateForm = createUpdateForm(commentId, currentContent);
            commentItem.appendChild(updateForm);
        });
    });
};

// 댓글 삭제 이벤트 추가 함수
const addDeleteEvents = () => {
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', async (event) => {
            const commentId = event.target.getAttribute('data-id');
            const confirmDelete = confirm('정말 삭제하시겠습니까?');
            if (confirmDelete) {
                try {
                    await axios.delete(`community/live/${liveId}/delete_comment/`, { data: { comment_id: commentId } });
                    alert('댓글 삭제 성공!');
                    getLiveDetail();  // 댓글 삭제 후 갱신
                } catch (error) {
                    console.error("Error:", error);
                    alert('댓글 삭제 실패');
                }
            }
        });
    });
};

// 댓글 좋아요 이벤트 추가 함수
const addLikeEvents = () => {
    document.querySelectorAll('.like-comment-button').forEach(button => {
        button.addEventListener('click', async (event) => {
            const commentId = event.target.getAttribute('data-id');
            const likeButton = event.target.closest('.like-comment-button');
            const likeCountElement = likeButton.querySelector('.like-count');
            try {
                const response = await axios.post(`community/live/${liveId}/toggle_like_comment/`, { comment_id: commentId });
                if (response.status === 201) {
                    alert('댓글 좋아요 성공!');
                } else if (response.status === 204) {
                    alert('댓글 좋아요 취소!');
                }
                getLiveDetail();  // 좋아요 상태 갱신
            } catch (error) {
                console.error("Error:", error);
                alert('댓글 좋아요 실패');
            }
        });
    });
};

// 대댓글 작성 폼 생성 함수
const createReplyForm = (parentId) => {
    const replyForm = document.createElement('form');
    replyForm.classList.add('reply-form');
    replyForm.innerHTML = `
        <textarea class="reply-content" placeholder="대댓글을 입력하세요" rows="2"></textarea>
        <button type="submit">대댓글 작성</button>
    `;
    replyForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const content = replyForm.querySelector('.reply-content').value;
        try {
            await axios.post(`community/live/${liveId}/create_comment/`, { content, parent_id: parentId });
            alert('대댓글 작성 성공!');
            getLiveDetail();  // 대댓글 작성 후 갱신
        } catch (error) {
            console.error("Error:", error);
            alert('대댓글 작성 실패');
        }
    });
    return replyForm;
};

// 댓글 수정 폼 생성 함수
const createUpdateForm = (commentId, currentContent) => {
    const updateForm = document.createElement('form');
    updateForm.classList.add('update-form');
    updateForm.innerHTML = `
        <textarea class="update-content" rows="2">${currentContent}</textarea>
        <button type="submit">수정 완료</button>
        <button type="button" class="cancel-button">취소</button>
    `;
    updateForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const content = updateForm.querySelector('.update-content').value;
        try {
            await axios.put(`community/live/${liveId}/update_comment/`, { comment_id: commentId, content });
            alert('댓글 수정 성공!');
            getLiveDetail();  // 댓글 수정 후 갱신
        } catch (error) {
            console.error("Error:", error);
            alert('댓글 수정 실패');
        }
    });

    // 취소 버튼 이벤트 처리
    updateForm.querySelector('.cancel-button').addEventListener('click', function() {
        updateForm.remove();  // 수정 폼 제거
    });

    return updateForm;
};

// 글 상세 (+ 댓글) 가져오기 함수
const getLiveDetail = async () => {
    try {
        const response = await axios.get(`community/live/${liveId}/`);
        const live = response.data;

        document.getElementById('live-author').innerText = live.author.nickname;
        document.getElementById('game-teams').innerText = `${live.home_team} vs ${live.away_team}`;
        document.getElementById('live-stadium').innerText = live.stadium;
        document.getElementById('live-game-date').innerText = new Date(live.game_date).toLocaleDateString();
        document.getElementById('live-seat').innerText = live.seat || "정보 없음";
        document.getElementById('live-review').innerText = live.review;

        // profile_image
        const profileImageElement = document.getElementById('live-profile-image');
        profileImageElement.src = live.author.profile_image ? live.author.profile_image.replace(/.*\/media/, '/media') : 'https://i.imgur.com/CcSWvhq.png';
        profileImageElement.alt = '프로필 이미지';

        // live_image
        const liveImageElement = document.getElementById('live-image');
        liveImageElement.src = live.live_image ? live.live_image.replace(/.*\/media/, '/media') : 'https://via.placeholder.com/300';
        liveImageElement.alt = '게시글 이미지';

        // 좋아요, 댓글 수, 작성일
        document.getElementById('like-count').innerText = live.likes_count;
        document.getElementById('comment-count').innerText = live.comments_count;
        document.getElementById('live-created-at').innerText = new Date(live.created_at).toLocaleString();

        // 좋아요, 북마크 상태 반영
        const likeIcon = document.getElementById('like-button');
        const likeText = document.getElementById('like-text');
        if (live.is_liked) {
            likeIcon.classList.add('active');
            likeText.classList.add('active');
        } else {
            likeIcon.classList.remove('active');
            likeText.classList.remove('active');
        }

        const bookmarkIcon = document.querySelector('.bookmark-icon');
        const bookmarkText = document.getElementById('bookmark-text');
        if (live.is_bookmarked) {
            bookmarkIcon.classList.add('active');
            bookmarkText.classList.add('active');
        } else {
            bookmarkIcon.classList.remove('active');
            bookmarkText.classList.remove('active');
        }

        // 댓글 목록 불러오기
        getComments(live.comments);

        // 로그인한 사람 유저네임 가져와
        const loggedInUsername = localStorage.getItem('username');

        // 작성자가 아니라면 수정/삭제 버튼 숨기기
        if (live.author.username !== loggedInUsername) {
            document.getElementById('update-button').style.display = 'none';
            document.getElementById('delete-button').style.display = 'none';
        }

        // 작성자 닉네임 클릭 -> 프로필 페이지로 이동
        const authorElement = document.getElementById('live-author');
        authorElement.onclick = () => {

        // Username = null (로그인 안된경우)
        if (!loggedInUsername) {
        location.href = `user_other_profile.html?username=${free.author.username}`;
        return;  // 남의 프로필
        }

        // 로그인 되어있는 경우
            if (live.author.username === loggedInUsername) {
                // 내 프로필
                location.href = `user_my_profile.html?username=${live.author.username}`;
            } else {
                // 남의 프로필
                location.href = `user_other_profile.html?username=${live.author.username}`;
            }
        };

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
document.querySelector('.bookmark-icon').addEventListener('click', async function() {

    if (!checkSignin()) return;

    try {
        const response = await axios.post(`community/live/${liveId}/toggle_bookmark/`);
        const bookmarkIcon = document.querySelector('.bookmark-icon');
        const bookmarkText = document.getElementById('bookmark-text');

        if (response.status === 201) {
            alert('이 글을 북마크할게요!!!!!');
            bookmarkIcon.classList.add('active');
            bookmarkText.classList.add('active');
        } else if (response.status === 204) {
            alert('이 글을 북마크하기 싫어졌음.');
            bookmarkIcon.classList.remove('active');
            bookmarkText.classList.remove('active');
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
        const likeIcon = document.getElementById('like-button');
        const likeText = document.getElementById('like-text');

        if (response.status === 201) {
            alert('이 글을 좋아할게요!!!!!');
            likeIcon.classList.add('active');
            likeText.classList.add('active');
        } else if (response.status === 204) {
            alert('이제 이 글을 더이상 좋아하지 않음.');
            likeIcon.classList.remove('active');
            likeText.classList.remove('active');
        }
        getLiveDetail(); // 좋아요 수 업데이트 (방금 내가 누른 좋아요 반영)

    } catch (error) {
        console.error("Error:", error);
        alert('좋아요 요청 실패');
    }
});