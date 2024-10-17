// URL에서 쿼리 파라미터로부터 username 추출
const username = new URLSearchParams(window.location.search).get('username');
if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다.');
}

// 프로필 데이터를 불러오기
const getProfileDetailForUpdate = async () => {
    try {
        const response = await axios.get(`user/${username}/`);
        const profile = response.data;
        document.getElementById('nickname').value = profile.nickname;
        document.getElementById('bio').value = profile.bio;

        if (profile.profile_image) {
            const imgPreview = document.getElementById('profile_image_preview');
            imgPreview.src = profile.profile_image;
            imgPreview.style.display = 'block'; // 이미지 미리보기 표시
        }
    } catch (error) {
        console.error("프로필 데이터를 불러오는 중 오류 발생:", error);
        alert('프로필 데이터를 불러오는 중 오류가 발생했습니다.');
    }
};

// 이미지 미리보기 설정
const profileImageInput = document.getElementById('profile_image');
profileImageInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const imgPreview = document.getElementById('profile_image_preview');
        imgPreview.src = URL.createObjectURL(file);  // 선택한 파일을 미리보기로 변환
        imgPreview.style.display = 'block';  // 이미지 미리보기 표시
    }
});

// 프로필 업데이트
const form = document.getElementById('profile-update-form');
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const nickname = document.getElementById('nickname').value;
    const bio = document.getElementById('bio').value;
    const profileImage = profileImageInput.files[0]; 

    const formData = new FormData();
    formData.append('nickname', nickname);
    formData.append('bio', bio);
    if (profileImage) {
        formData.append('profile_image', profileImage);  // 프로필 이미지 추가
    }

    try {
        await axios.put(`user/${username}/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        alert('프로필 수정 완료!');
        location.href = `user_main_profile.html?username=${username}`;
    } catch (error) {
        console.error("프로필 수정 중 오류 발생:", error);
        alert('프로필 수정 실패');
    }
});

// 취소 버튼 클릭 시 이전 페이지로 이동
const cancelButton = document.getElementById('cancel-button');
cancelButton.addEventListener('click', () => {
    window.history.back();
});


// 페이지 로드 시 프로필 데이터 불러오기
document.addEventListener('DOMContentLoaded', getProfileDetailForUpdate);
