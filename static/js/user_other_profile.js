// URL에서 쿼리 파라미터로부터 username 추출
const params = new URLSearchParams(window.location.search);
const username = params.get('username'); // URL에서 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 페이지네이션 관련 변수
let currentPage = 1;
const itemsPerPage = 6; // 페이지 당 이미지 6개

// 프로필 정보 및 직관인증 이미지 가져오는 함수
async function getUserProfile() {
    try {
        const response = await axios.get(`user/${username}/`); // API 요청
        const data = response.data;

        // 프로필 이미지
        const profileImage = document.getElementById('profileImage');
        profileImage.src = data.profile_image || 'https://via.placeholder.com/150';

        // 닉네임 
        const nicknameElement = document.querySelector('.nickname');
        nicknameElement.textContent = data.nickname;

        // 팔로워 및 팔로잉 수 설정 및 링크 추가
        const followersLink = document.getElementById('followers-link');
        const followingLink = document.getElementById('following-link');
        followersLink.innerHTML = `${data.followers_count} followers`;  // 팔로워 수 추가
        followingLink.innerHTML = `${data.following_count} following`;  // 팔로잉 수 추가
        followersLink.href = `user_followerlist.html?username=${data.username}`;
        followingLink.href = `user_followlist.html?username=${data.username}`;
        
        // 소개글(bio) 설정
        const bioElement = document.getElementById('bio');
        bioElement.textContent = data.bio || '소개글이 없습니다.';

        // 갤러리 이미지 설정
        renderGallery(data.community_live_image);

    } catch (error) {
        console.error('프로필 정보를 가져오는 중 오류 발생:', error);
        alert('프로필 정보를 불러오는 중 오류가 발생했습니다.');
    }
}

// 갤러리 이미지를 페이지네이션하여 표시하는 함수
function renderGallery(images) {
    const galleryContainer = document.querySelector('.gallery');
    galleryContainer.innerHTML = ''; // 기존 이미지 초기화

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const currentImages = images.slice(start, end); // 현재 페이지에 해당하는 이미지 선택

    currentImages.forEach(image => {
        const galleryItem = document.createElement('div');
        galleryItem.classList.add('gallery-item');
        
        // 이미지 엘리먼트 생성
        const imgElement = document.createElement('img');
        imgElement.src = image.url || 'https://via.placeholder.com/150'; // 이미지 URL 설정
        imgElement.onerror = () => {
            imgElement.src = 'https://via.placeholder.com/150'; // 이미지 로드 실패 시 기본 이미지 설정
        };

        // 타임스탬프 표시
        const timestamp = document.createElement('div');
        timestamp.classList.add('timestamp');
        timestamp.textContent = image.created_at;

        // 클릭 이벤트 (직관 게시글로 이동)
        galleryItem.addEventListener('click', () => {
            window.location.href = `live_detail.html?id=${image.id}`; // 상세 페이지로 이동
        });

        galleryItem.appendChild(imgElement);
        galleryItem.appendChild(timestamp);
        galleryContainer.appendChild(galleryItem);
    });

    // 페이지네이션 버튼 상태 업데이트
    document.getElementById('prev-button').disabled = currentPage === 1;
    document.getElementById('next-button').disabled = end >= images.length;
}

// 이전 페이지 버튼 클릭 시 이벤트
document.getElementById('prev-button').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        getUserProfile(); // 페이지 이동 후 다시 데이터 가져오기
    }
});

// 다음 페이지 버튼 클릭 시 이벤트
document.getElementById('next-button').addEventListener('click', () => {
    currentPage++;
    getUserProfile(); // 페이지 이동 후 다시 데이터 가져오기
});

// 페이지 로드 시 프로필 정보 및 갤러리 데이터 가져오기
document.addEventListener('DOMContentLoaded', getUserProfile);


// 팔로우 토글
document.getElementById('follow-button').addEventListener('click', async function() {

    if (!checkSignin()) return;

    try {
        const response = await axios.post(`user/${username}/follow/`);

        // 팔로우
        if (response.data === '팔로우성공!') {
            alert('팔로우했습니다!');
            document.getElementById('follow-button').textContent = '팔로우 취소하기';
        } else if (response.data === '언팔로우!') {
            alert('팔로우가 취소되었습니다!');
            document.getElementById('follow-button').textContent = '팔로우하기';
        }
        await getUserProfile();  // 방금 팔로우 반영한 followers 수 표시

    } catch (error) {
        console.error("Error:", error);
        alert('팔로우 요청 실패');
    }
});