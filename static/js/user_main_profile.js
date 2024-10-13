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
        const profileImage = document.querySelector('.profile-image');
        profileImage.src = data.profile_image || 'https://via.placeholder.com/150';

        // 닉네임 설정
        const nicknameElement = document.querySelector('.nickname');
        nicknameElement.textContent = data.nickname;

        // 소개글(bio) 설정
        const bioElement = document.querySelector('.bio p');
        bioElement.textContent = data.bio || '소개글이 없습니다.';

        // 이메일 및 전화번호 설정
        const emailElement = document.querySelector('.contact-info p:nth-child(1)');
        const phoneNumberElement = document.querySelector('.contact-info p:nth-child(2)');
        emailElement.textContent = `email: ${data.email || '등록된 이메일이 없습니다.'}`;
        phoneNumberElement.textContent = `전화번호: ${data.phone_number || '등록된 전화번호가 없습니다.'}`;

        // 가입일 설정
        const signupDateElement = document.querySelector('.signup-date');
        signupDateElement.textContent = `가입일: ${data.created_at.split('T')[0]}`;

        // 팔로워 및 팔로잉 수 설정 및 링크 추가
        const followerInfoElement = document.querySelector('.follower-info');
        followerInfoElement.innerHTML = `<a href="followers.html">${data.followers_count} followers</a> · <a href="following.html">${data.following_count} following</a>`;

        // 통계 데이터 설정 (커뮤니티 작성글, 댓글, 자게 작성글, 좋아요한 글)
        const stats = document.querySelectorAll('.stat-number');
        stats[0].textContent = `${data.article_count}개`;  // 커뮤니티 작성글
        stats[1].textContent = `${data.comment_count}개`;  // 작성 댓글
        stats[2].textContent = `${data.article_count}개`;  // 자게 작성글 (자게 글도 article_count로 처리)
        stats[3].textContent = `${data.bookmark_count}개`;  // 좋아요한 글
    } catch (error) {
        console.error('프로필 정보를 가져오는 중 오류 발생:', error);
        alert('프로필 정보를 불러오는 중 오류가 발생했습니다.');
    }
}

// 페이지 로드 시 사용자 프로필 데이터 가져오기
document.addEventListener('DOMContentLoaded', getUserProfile);
