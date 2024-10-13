// URL에서 쿼리 파라미터로부터 username 추출하기
const params = new URLSearchParams(window.location.search);
const username = params.get('username');  // URL에서 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 사용자 정보와 작성 직관인증 이미지를 가져오는 함수
const loadUserProfileAndImages = async () => {
    try {
        // 서버로부터 사용자 정보와 작성 글 목록 가져오기
        const response = await axios.get(`user/${username}/live/`);
        const userData = response.data;

        // 프로필 이미지와 닉네임 설정
        document.getElementById('profile-image').src = userData.profile_image;
        document.getElementById('nickname').textContent = userData.nickname;

        // 작성한 직관인증 글의 이미지 리스트 추가
        const postsList = document.getElementById('live-posts-list');
        userData.community_live_image.forEach(imageUrl => {
            const listItem = document.createElement('li');
            const imgElement = document.createElement('img');
            imgElement.src = imageUrl;
            imgElement.alt = '직관인증 이미지';
            imgElement.style.width = '100px';
            imgElement.style.height = '100px';
            listItem.appendChild(imgElement);
            postsList.appendChild(listItem);
        });

    } catch (error) {
        console.error("작성 글 데이터를 불러오는 중 오류 발생:", error);
        alert('작성 글 데이터를 불러오는 중 오류가 발생했습니다.');
    }
};

// mypage 버튼 클릭 시 페이지 이동 설정
document.getElementById('mypage-button').addEventListener('click', () => {
    window.location.href = `user_main_profile.html?username=${username}`;
});

// 버튼 버튼 클릭 시 페이지 이동 설정
document.getElementById('free_posts-button').addEventListener('click', () => {
    window.location.href = `user_free_list.html?username=${username}`;
});
document.getElementById('comments-button').addEventListener('click', () => {
    window.location.href = `user_comment_list.html?username=${username}`;
});
document.getElementById('saved_posts-button').addEventListener('click', () => {
    window.location.href = `user_bookmark_list.html?username=${username}`;
});


// 페이지 로드 시 사용자 정보와 작성 직관인증 이미지를 불러옴
document.addEventListener('DOMContentLoaded', loadUserProfileAndImages);
