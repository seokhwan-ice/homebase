// URL에서 쿼리 파라미터로부터 username 추출하기
const params = new URLSearchParams(window.location.search);
const username = params.get('username');  // URL에서 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 프로필 정보 및 통계 데이터를 가져오기 위한 함수
async function getUserProfile() {
    try {
        const response = await axios.get(`user/${username}/`);
        const data = response.data;

        // 프로필 이미지 설정
        const profileImage = document.getElementById('profileImage');
        profileImage.src = data.profile_image || 'https://via.placeholder.com/150';

        // 닉네임 설정
        const nicknameElement = document.getElementById('nickname');
        nicknameElement.textContent = data.nickname;

        // 소개글(bio) 설정
        const bioElement = document.getElementById('bio');
        bioElement.textContent = data.bio || '소개글이 없습니다.';

        // 이메일 및 전화번호 설정
        const emailElement = document.getElementById('email');
        const phoneNumberElement = document.getElementById('phone-number');
        emailElement.textContent = `email: ${data.email || '등록된 이메일이 없습니다.'}`;
        phoneNumberElement.textContent = `전화번호: ${data.phone_number || '등록된 전화번호가 없습니다.'}`;

        // 가입일 설정
        const signupDateElement = document.getElementById('signup-date');
        signupDateElement.textContent = `가입일: ${data.created_at}`;

        // 팔로워 및 팔로잉 수 설정 및 링크 추가
        const followersLink = document.getElementById('followers-link');
        const followingLink = document.getElementById('following-link');
        followersLink.innerHTML = `${data.followers_count} followers`;  // 팔로워 수 추가
        followingLink.innerHTML = `${data.following_count} following`;  // 팔로잉 수 추가
        followersLink.href = `user_followerlist.html?username=${data.username}`;
        followingLink.href = `user_followlist.html?username=${data.username}`;
        
        // 통계 데이터 설정 (커뮤니티 작성글, 댓글, 자게 작성글, 좋아요한 글)
        const communityCountElement = document.getElementById('community-count');
        const commentCountElement = document.getElementById('comment-count');
        const freeboardCountElement = document.getElementById('freeboard-count');
        const likedCountElement = document.getElementById('liked-count');
        
        communityCountElement.textContent = `${data.article_count}개`;
        commentCountElement.textContent = `${data.comment_count}개`;
        freeboardCountElement.textContent = `${data.article_count}개`; 
        likedCountElement.textContent = `${data.bookmark_count}개`;

        // 링크 설정
        document.getElementById('community-link').href = `user_live_list.html?username=${data.username}`;
        document.getElementById('comment-link').href = `user_comment_list.html?username=${data.username}`;
        document.getElementById('freeboard-link').href = `user_free_list.html?username=${data.username}`;
        document.getElementById('bookmark-link').href = `user_bookmark_list.html?username=${data.username}`;

        // edit profile, edit profile (public) 버튼 클릭 시 페이지 이동 설정
        document.getElementById('edit-public-profile').addEventListener('click', () => {
            window.location.href = `user_pubprofile_update.html?username=${data.username}`;
        });
        document.getElementById('edit-profile').addEventListener('click', () => {
            window.location.href = `user_prvprofile_update.html?username=${data.username}`;
        });

    } catch (error) {
        console.error('프로필 정보를 가져오는 중 오류 발생:', error);
        alert('프로필 정보를 불러오는 중 오류가 발생했습니다.');
    }
}

// 페이지 로드 시 사용자 프로필 데이터 가져오기
document.addEventListener('DOMContentLoaded', getUserProfile);
