// URL에서 쿼리 파라미터로부터 username 추출하기
const params = new URLSearchParams(window.location.search);
const username = params.get('username');  // URL에 있는 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 프로필 데이터를 불러오기
const getProfileDetailForUpdate = async () => {
    try {
        const response = await axios.get(`user/${username}/`);  // 프로필 데이터를 GET 요청으로 가져옴
        const profile = response.data;

        // 가져온 데이터를 폼에 반영
        document.getElementById('nickname').value = profile.nickname;
        document.getElementById('bio').value = profile.bio;

        // 프로필 이미지가 있을 경우 표시
        if (profile.profile_image) {
            const imgPreview = document.getElementById('profile_image_preview');
            imgPreview.src = profile.profile_image;
            imgPreview.style.display = 'block';  // 이미지 미리보기 표시
        }
    } catch (error) {
        console.error("프로필 데이터를 불러오는 중 오류 발생:", error);
        alert('프로필 데이터를 불러오는 중 오류가 발생했습니다.');
    }
};

// 이미지 미리보기 설정
const profileImageInput = document.getElementById('profile_image');
profileImageInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const imgPreview = document.getElementById('profile_image_preview');
        imgPreview.src = URL.createObjectURL(file);  // 선택한 파일을 미리보기로 변환
        imgPreview.style.display = 'block';  // 이미지 미리보기 표시
    }
});

// 프로필 업데이트
const form = document.getElementById('profile-update-form');
form.addEventListener('submit', async function(event) {
    event.preventDefault();  // 폼 제출 방지

    const nickname = document.getElementById('nickname').value;
    const bio = document.getElementById('bio').value;
    const profileImage = document.getElementById('profile_image').files[0];  // 파일 선택

    const formData = new FormData();
    formData.append('nickname', nickname);
    formData.append('bio', bio);
    if (profileImage) {
        formData.append('profile_image', profileImage);  // 프로필 이미지 추가
    }

    try {
        const response = await axios.put(`user/${username}/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'  // 파일 업로드를 위해 설정
            }
        });  // 프로필 업데이트 요청
        alert('프로필 수정 완료!');
        location.href = `user_profile.html?username=${username}`;  // 수정 완료 후 프로필 페이지로 이동
    } catch (error) {
        console.error("프로필 수정 중 오류 발생:", error);
        alert('프로필 수정 실패');
    }
});

// 취소 버튼 클릭 시 이전 페이지로 이동
document.getElementById('cancel-button').addEventListener('click', function() {
    if (document.referrer) {
        window.history.back();  // 이전 페이지로 이동
    } else {
        location.href = 'home.html';  // 이전 페이지가 없을 경우 홈 페이지로 이동
    }
});
// 홈 페이지 지정시 >>>>>>>>>>>>> 수정해야함 >>> >

// 페이지 로드 시 프로필 데이터 불러오기
document.addEventListener('DOMContentLoaded', getProfileDetailForUpdate);

