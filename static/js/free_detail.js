
const params = new URLSearchParams(location.search);
const freeId = params.get('id');

// 댓글 목록 가져오기 함수
const getComments = (comments) => {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = ''; // 댓글 목록 초기화

    comments.forEach(comment => {
        const commentItem = createCommentItem(comment);  // 댓글 생성 함수호출
        commentsList.appendChild(commentItem);

        // 대댓글 있다면
        if (comment.replies) {
            getReplies(comment.replies, comment.id);  // 대댓글 목록 가져오기 함수 호출
        }
    });

    addReplyEvents();  // 댓글 작성 함수호출
    addUpdateEvents();  // 댓글 수정 함수호출
    addDeleteEvents();  // 댓글 삭제 함수호출
};

// 대댓글 목록 가져오기 함수
const getReplies = (replies, parentId) => {
    const replyList = document.getElementById(`reply-list-${parentId}`);
    replies.forEach(reply => {
        const replyItem = createCommentItem(reply);  // 대댓글 생성 함수호출
        replyList.appendChild(replyItem);

        // 대대ㅐㅐ댓글 가져오기
        if (reply.replies && reply.replies.length > 0) {
            getReplies(reply.replies, reply.id); // 재귀적으로 가져오기!!!!
        }
    });
};

// 대.댓글 생성 함수
const createCommentItem = (comment) => {
    const commentItem = document.createElement('div');
    commentItem.classList.add('comment-item');

    commentItem.innerHTML = `
        <div class="comment-header">
            <div class="comment-author-info">
                <img class="comment-profile-image" src="${comment.author.profile_image}" alt="프로필 이미지">
                <span class="comment-author">${comment.author.nickname}</span>
            </div>
            <span class="comment-time">${new Date(comment.created_at).toLocaleString()}</span>
        </div>
        <div class="comment-body">
            <div class="comment-content">${comment.content}</div>
            <div class="comment-buttons">
                <button class="reply-button" data-id="${comment.id}">답글</button>
                <button class="update-button" data-id="${comment.id}">수정</button>
                <button class="delete-button" data-id="${comment.id}">삭제</button>
            </div>
        </div>
        <hr class="comment-hr">
        <div class="reply-list" id="reply-list-${comment.id}"></div>
    `;
    return commentItem;
};

// 댓글 작성 함수
const addReplyEvents = () => {
    document.querySelectorAll('.reply-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const parentId = event.target.getAttribute('data-id');
            const replyForm = createReplyForm(parentId); // 대댓글 폼 생성 함수호출
            document.getElementById(`reply-list-${parentId}`).appendChild(replyForm);
        });
    });
};

// 댓글 수정 함수
const addUpdateEvents = () => {
    document.querySelectorAll('.update-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const commentId = event.target.getAttribute('data-id');
            const commentItem = event.target.parentElement;
            const currentContent = commentItem.querySelector('p').textContent;
            const updateForm = createUpdateForm(commentId, currentContent); // 수정 폼 생성 함수호출
            commentItem.appendChild(updateForm);
        });
    });
};

// 댓글 삭제 함수
const addDeleteEvents = () => {
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', async (event) => {
            const commentId = event.target.getAttribute('data-id');
            if (confirm('정말 삭제하시겠습니까?????')) {
                try {
                    await axios.delete(`community/free/${freeId}/delete_comment/`, { data: { comment_id: commentId } });
                    alert('댓글 삭제 성공!');
                    getFreeDetail(); // 삭제 후 목록 갱신
                } catch (error) {
                    console.error("Error:", error);
                    alert('댓글 삭제 실패');
                }
            }
        });
    });
};

// 대댓글 작성 폼 생성 함수
const createReplyForm = (parentId) => {
    const replyForm = document.createElement('form');
    replyForm.classList.add('reply-form');
    replyForm.innerHTML = `
        <textarea class="reply-content" placeholder="대댓글을 입력하게요" rows="2"></textarea>
        <button type="submit">대댓글 작성</button>
    `;
    replyForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const content = replyForm.querySelector('.reply-content').value;
        const formData = { content, parent_id: parentId };
        try {
            await axios.post(`community/free/${freeId}/create_comment/`, formData);
            alert('대댓글 작성 성공!');
            getFreeDetail(); // 대댓글 작성 후 목록 갱신
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
    `;
    updateForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const content = updateForm.querySelector('.update-content').value;
        const formData = { comment_id: commentId, content };
        try {
            await axios.put(`community/free/${freeId}/update_comment/`, formData);
            alert('댓글 수정 성공!!!');
            getFreeDetail(); // 수정 후 목록 갱신
        } catch (error) {
            console.error("Error:", error);
            alert('댓글 수정 실패');
        }
    });
    return updateForm;
};

// 글 상세 (+ 댓글) 가져오기 함수
const getFreeDetail = async () => {
    try {
        const response = await axios.get(`community/free/${freeId}/`);
        const free = response.data;

        document.getElementById('free-title').textContent = free.title;
        document.getElementById('free-author').textContent = free.author.nickname;
        document.getElementById('free-created-at').textContent = new Date(free.created_at).toLocaleString();
        document.getElementById('free-updated-at').textContent = new Date(free.updated_at).toLocaleString();
        document.getElementById('free-content').textContent = free.content;
        document.getElementById('free-views').textContent = free.views;
        document.getElementById('free-comments-count').textContent = free.comments_count;

        const profileImage = document.getElementById('free-profile-image');
        if (free.author.profile_image) {
            profileImage.src = free.author.profile_image;
            profileImage.style.display = 'block';
        }

        const freeImage = document.getElementById('free-image');
        if (free.free_image) {
            freeImage.src = free.free_image;
            freeImage.style.display = 'block';
        }

        // 북마크 상태 반영
        const bookmarkIcon = document.getElementById('bookmark-icon');
        const bookmarkText = document.getElementById('bookmark-text');
        if (free.is_bookmarked) {
            bookmarkIcon.classList.add('active');
            bookmarkText.classList.add('active');
        } else {
            bookmarkIcon.classList.remove('active');
            bookmarkText.classList.remove('active');
        }

        // 댓글 목록 불러오기
        getComments(free.comments);

    } catch (error) {
        console.error("Error:", error);
        alert("글 상세 정보 불러오기 실패");
    }
};

// 댓글 등록
const commentForm = document.getElementById('comment-form');
commentForm.addEventListener('submit', async function(event) {
    event.preventDefault();
    if (!checkSignin()) return;

    const content = document.getElementById('comment-content').value;
    const formData = { content };
    try {
        await axios.post(`community/free/${freeId}/create_comment/`, formData);
        alert('댓글 작성 성공!');
        getFreeDetail(); // 방금 내가 쓴 댓글 반영
        document.getElementById('comment-content').value = ''; // 입력창 초기화
    } catch (error) {
        console.error("Error:", error);
        alert('댓글 작성 실패');
    }
});


// 글 수정
document.getElementById('update-button').addEventListener('click', function() {
    if (!checkSignin()) return;
    location.href = `free_update.html?id=${freeId}`;
});

// 글 삭제
document.getElementById('delete-button').addEventListener('click', async function() {
    if (!checkSignin()) return;
    if (confirm('정말 삭제하시겠어요?????')) {
        try {
            await axios.delete(`community/free/${freeId}/`);
            alert('글이 삭제되었습니다!');
            location.href = 'free_list.html'; // 삭제 후 목록 페이지로 이동
        } catch (error) {
            console.error('Error:', error);
            alert('글 삭제 실패');
        }
    }
});

// 북마트 토글
document.getElementById('bookmark-icon').addEventListener('click', async function() {
    if (!checkSignin()) return;
    try {
        const response = await axios.post(`community/free/${freeId}/toggle_bookmark/`);
        const bookmarkIcon = document.getElementById('bookmark-icon');
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

getFreeDetail();