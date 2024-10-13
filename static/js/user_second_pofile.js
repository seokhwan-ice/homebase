// URL에서 쿼리 파라미터로부터 username 추출하기
const params = new URLSearchParams(window.location.search);
const username = params.get('username'); // URL에서 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 페이지네이션 관련 변수
let currentPage = 1;
const itemsPerPage = 6; // 6개의 이미지씩 페이지네이션

// 프로필 정보 및 이미지 데이터를 가져오는 함수
async function getUserProfile() {
    try {
        const response = await axios.get(`user/${username}/`);
        const data = response.data;

        // 프로필 이미지 설정
        const profileImage = document.querySelector('.profile-image');
        profileImage.style.backgroundImage = `url(${data.profile_image || 'https://via.placeholder.com/150'})`;

        // 닉네임 설정
        const nicknameElement = document.querySelector('.nickname');
        nicknameElement.textContent = data.nickname;

        // 팔로워 및 팔로잉 수 설정 및 링크 추가
        const followerInfoElement = document.querySelector('.follower-info');
        followerInfoElement.innerHTML = `<a href="followers.html">${data.follower_count} followers</a> · <a href="following.html">${data.following_count} following</a>`;

        // 커뮤니티 라이브 이미지 설정
        renderGallery(data.community_live_image);
    } catch (error) {
        console.error('프로필 정보를 가져오는 중 오류 발생:', error);
        alert('프로필 정보를 불러오는 중 오류가 발생했습니다.');
    }
}

// 갤러리 페이지네이션 함수
function renderGallery(images) {
    const galleryContainer = document.querySelector('.gallery');
    galleryContainer.innerHTML = ''; // 기존 이미지 초기화

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const currentImages = images.slice(start, end);

    currentImages.forEach((imageUrl) => {
        const imgElement = document.createElement('img');
        imgElement.src = imageUrl || 'https://via.placeholder.com/150'; // 기본 이미지 제공
        imgElement.onerror = () => {
            imgElement.src = 'https://via.placeholder.com/150'; // 이미지 로드 실패 시 기본 이미지 제공
        };
        galleryContainer.appendChild(imgElement);
    });

    // 페이지네이션 버튼 상태 업데이트
    document.getElementById('prev-button').disabled = currentPage === 1;
    document.getElementById('next-button').disabled = end >= images.length;
}

// 이전 페이지 버튼 클릭 이벤트 핸들러
document.getElementById('prev-button').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        getUserProfile(); // 페이지 변경 후 데이터 다시 가져오기
    }
});

// 다음 페이지 버튼 클릭 이벤트 핸들러
document.getElementById('next-button').addEventListener('click', () => {
    currentPage++;
    getUserProfile(); // 페이지 변경 후 데이터 다시 가져오기
});

// 페이지 로드 시 사용자 프로필 데이터 가져오기
document.addEventListener('DOMContentLoaded', getUserProfile);
