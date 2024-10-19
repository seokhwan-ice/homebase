
// 직관인증게시판 글 상세 (live_detail)

const params = new URLSearchParams(location.search);
const liveId = params.get('id');

// 댓글 목록 가져오기 함수
const getComments = (comments) => {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = '';  // 기존 댓글 초기화

    comments.forEach(comment => {
        const commentItem = document.createElement('div');
        commentItem.classList.add('comment-item');
        commentItem.innerHTML = `
            <p>작성자: ${comment.author.nickname}</p>
            <p>댓글내용: ${comment.content}</p>
            <p>작성시간: ${new Date(comment.created_at).toLocaleString()}</p>
            <p>좋아요수: ${comment.likes_count}</p>
            <button class="reply-button" data-id="${comment.id}">대댓글</button>
            <button class="update-button" data-id="${comment.id}">수정</button>
            <button class="delete-button" data-id="${comment.id}">삭제</button>
            <button class="like-comment-button" data-id="${comment.id}">댓글 좋아요</button>
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
                <textarea class="reply-content" placeholder="대댓글을 입력하세요" rows="2"></textarea>
                <button type="submit">대댓글 작성</button>
            `;
            document.getElementById(`reply-list-${parentId}`).appendChild(replyForm);

            replyForm.addEventListener('submit', async function(event) {
                event.preventDefault();
                const content = replyForm.querySelector('.reply-content').value;
                const formData = { content, parent_id: parentId };

                try {
                    await axios.post(`community/live/${liveId}/create_comment/`, formData);
                    alert('대댓글 작성 성공!');
                    getLiveDetail();
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
                    await axios.put(`community/live/${liveId}/update_comment/`, formData);
                    alert('댓글 수정 성공!');
                    getLiveDetail(); // 수정된 댓글 반영
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
            const confirmDelete = confirm('정말 삭제하시겠습니까?');
            if (confirmDelete) {
                try {
                    await axios.delete(`community/live/${liveId}/delete_comment/`, { data: { comment_id: commentId } });
                    alert('댓글 삭제 성공!');
                    getLiveDetail(); // 삭제된 댓글 반영
                } catch (error) {
                    console.error("Error:", error);
                    alert('댓글 삭제 실패');
                }
            }
        });
    });

    // 댓글 좋아요 버튼 이벤트 추가
    document.querySelectorAll('.like-comment-button').forEach(button => {
        button.addEventListener('click', async (event) => {
            const commentId = event.target.getAttribute('data-id');

            try {
                const response = await axios.post(`community/live/${liveId}/toggle_like_comment/`, { comment_id: commentId });
                if (response.status === 201) {
                    alert('댓글 좋아요 성공!');
                } else if (response.status === 204) {
                    alert('댓글 좋아요 취소!');
                }
                getLiveDetail(); // 좋아요 수 업데이트
            } catch (error) {
                console.error("Error:", error);
                alert('댓글 좋아요 실패');
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
            <p>좋아요수: ${reply.likes_count}</p>
            <button class="update-button" data-id="${reply.id}">수정</button>
            <button class="delete-button" data-id="${reply.id}">삭제</button>
            <button class="like-comment-button" data-id="${reply.id}">댓글 좋아요</button>
            <hr>
        `;
        replyList.appendChild(replyItem);
    });
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

        // // profile_image
        // const profileImageElement = document.getElementById('live-profile-image');
        // profileImageElement.src = live.author.profile_image || 'https://i.imgur.com/CcSWvhq.png';
        // profileImageElement.alt = '프로필 이미지';
        //
        // // live_image
        // const liveImageElement = document.getElementById('live-image');
        // liveImageElement.src = live.live_image || 'https://via.placeholder.com/300';
        // liveImageElement.alt = '게시글 이미지';

        // profile_image
        const profileImage = document.getElementById('live-profile-image');
        if (live.author.profile_image) {
            const profileImageUrl = live.author.profile_image.split(',');
            const cleanProfileImage = profileImageUrl[0] + profileImageUrl[1].substring(profileImageUrl[1].indexOf('/'));
            profileImage.src = cleanProfileImage;
        } else {
            profileImage.src = 'https://i.imgur.com/CcSWvhq.png';
        }
        profileImage.alt = '프로필 이미지';

        // live_image
        const liveImage = document.getElementById('live-image');
        const liveImageUrl = live.live_image.split(',');
        const cleanLiveImage = liveImageUrl[0] + liveImageUrl[1].substring(liveImageUrl[1].indexOf('/'));
        liveImage.src = cleanLiveImage;
        liveImage.alt = '게시글 이미지';

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
        // 작성자 닉네임 클릭 -> 프로필 페이지로 이동
        const authorElement = document.getElementById('live-author');
        authorElement.onclick = () => {
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