
const params = new URLSearchParams(location.search);
const freeId = params.get('id');

// 댓글 목록 가져오기 함수
const getComments = (comments) => {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = '';

    comments.forEach(comment => {
        const commentItem = document.createElement('div');
        commentItem.classList.add('comment-item');
        commentItem.innerHTML = `
            <p>작성자: ${comment.author.nickname}</p>
            <p>댓글내용: ${comment.content}</p>
            <p>작성시간: ${new Date(comment.created_at).toLocaleString()}</p>
            <button class="reply-button" data-id="${comment.id}">답글</button>
            <button class="update-button" data-id="${comment.id}">수정</button>
            <button class="delete-button" data-id="${comment.id}">삭제</button>
            <div class="reply-list" id="reply-list-${comment.id}"></div>
            <hr>
        `;
        commentsList.appendChild(commentItem);

        // 대댓글 표시
        if (comment.replies) {
            getReplies(comment.replies, comment.id);
        }
    });

    // 대댓글 달기 버튼 이벤트 추가
    document.querySelectorAll('.reply-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const parentId = event.target.getAttribute('data-id');
            const replyForm = document.createElement('form');
            replyForm.classList.add('reply-form');
            replyForm.innerHTML = `
                <textarea class="reply-content" placeholder="대댓글을 입력하게요" rows="2"></textarea>
                <button type="submit">대댓글 작성</button>
            `;
            document.getElementById(`reply-list-${parentId}`).appendChild(replyForm);

            replyForm.addEventListener('submit', async function(event) {
                event.preventDefault();
                const content = replyForm.querySelector('.reply-content').value;
                const formData = { content, parent_id: parentId };

                try {
                    await axios.post(`community/free/${freeId}/create_comment/`, formData);
                    alert('대댓글 작성 성공!');
                    getFreeDetail(); // 다시 불러와 (방금 작성한 대댓글 반영)
                } catch (error) {
                    console.error("Error:", error);
                    alert('대댓글 작성 실패');
                }
            });
        });
    });

    // 댓글 수정 버튼 이벤트 추가
    document.querySelectorAll('.update-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const commentId = event.target.getAttribute('data-id');
            const commentItem = event.target.parentElement;
            const currentContent = commentItem.querySelector('p:nth-child(2)').textContent.replace('댓글내용: ', '');
            const updateForm = document.createElement('form');
            updateForm.classList.add('update-form');
            updateForm.innerHTML = `
                <textarea class="update-content" rows="2">${currentContent}</textarea>
                <button type="submit">수정 완료</button>
            `;
            commentItem.appendChild(updateForm);

            updateForm.addEventListener('submit', async function(event) {
                event.preventDefault();
                const content = updateForm.querySelector('.update-content').value;
                const formData = { comment_id: commentId, content };

                try {
                    await axios.put(`community/free/${freeId}/update_comment/`, formData);
                    alert('댓글 수정 성공!!!');
                    getFreeDetail(); // 수정된 댓글 반영
                } catch (error) {
                    console.error("Error:", error);
                    alert('댓글 수정 실패');
                }
            });
        });
    });

    // 댓글 삭제 버튼 이벤트 추가
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', async (event) => {
            const commentId = event.target.getAttribute('data-id');
            const confirmDelete = confirm('정말 삭제하시겠습니까?????');
            if (confirmDelete) {
                try {
                    await axios.delete(`community/free/${freeId}/delete_comment/`, { data: { comment_id: commentId } });
                    alert('댓글 삭제 성공!');
                    getFreeDetail(); // 삭제된 댓글 반영
                } catch (error) {
                    console.error("Error:", error);
                    alert('댓글 삭제 실패');
                }
            }
        });
    });
};

// 대댓글 목록 가져오기 함수
const getReplies = (replies, parentId) => {
    const replyList = document.getElementById(`reply-list-${parentId}`);
    replies.forEach(reply => {
        const replyItem = document.createElement('div');
        replyItem.classList.add('reply-item');
        replyItem.innerHTML = `
            <p>작성자: ${reply.author.nickname}</p>
            <p>대댓글내용: ${reply.content}</p>
            <p>작성시간: ${new Date(reply.created_at).toLocaleString()}</p>
            <button class="update-button" data-id="${reply.id}">수정</button>
            <button class="delete-button" data-id="${reply.id}">삭제</button>
            <hr>
        `;
        replyList.appendChild(replyItem);
    });
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

// 댓글 등록
const commentForm = document.getElementById('comment-form');
commentForm.addEventListener('submit', async function(event) {
    event.preventDefault();

    if (!checkSignin()) return;

    const content = document.getElementById('comment-content').value;
    const formData = { content };

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


// 글 수정
document.getElementById('update-button').addEventListener('click', function() {

    if (!checkSignin()) return;

    location.href = `free_update.html?id=${freeId}`;  // 수정 페이지로 이동
});

// 글 삭제
document.getElementById('delete-button').addEventListener('click', async function() {

    if (!checkSignin()) return;

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

// 북마트 토글
document.getElementById('bookmark-button').addEventListener('click', async function() {

    if (!checkSignin()) return;

    try {
        const response = await axios.post(`community/free/${freeId}/toggle_bookmark/`);
        const bookmarkIcon = document.getElementById('bookmark-icon');

        // 북마크 상태에 따라 버튼 텍스트 변경 >>> 나중에 아이콘으로 바꾸쟈
        if (response.status === 201) {
            alert('글을 북마크했습니다!!!');
            bookmarkIcon.classList.add('active');
        } else if (response.status === 204) {
            alert('북마크를 취소했습니다!');
            bookmarkIcon.classList.remove('active');
        }

    } catch (error) {
        console.error("Error:", error);
        alert('북마크 요청 실패');
    }
});