// URL에서 쿼리 파라미터로부터 username 추출
const username = new URLSearchParams(window.location.search).get('username');
if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다.');
}

// 전화번호 형식 확인 함수
const isValidPhoneNumber = (phoneNumber) => {
    const phonePattern = /^010-?[1-9]\d{3}-\d{4}$/;
    return phonePattern.test(phoneNumber);
};

// 프로필 데이터를 불러오기
const getProfileDetailForUpdate = async () => {
    try {
        const response = await axios.get(`user/${username}/`);
        const profile = response.data;
        document.getElementById('current-email').textContent = profile.email || '등록된 이메일이 없습니다';
        document.getElementById('current-phone_number').textContent = profile.phone_number || '등록된 전화번호가 없습니다';
    } catch (error) {
        console.error("프로필 데이터를 불러오는 중 오류 발생:", error);
        alert('프로필 데이터를 불러오는 중 오류가 발생했습니다.');
    }
};

// 프로필 업데이트
document.getElementById('account-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const phone_number = document.getElementById('phone_number').value;

    const formData = {};

    if (email) {
        formData.email = email;
    }

    if (phone_number && isValidPhoneNumber(phone_number)) {
        formData.phone_number = phone_number;
    } else if (phone_number) {
        alert('010-XXXX-XXXX 형식으로 입력하세요.');
        return;
    }

    try {
        await axios.patch(`user/${username}/`, formData);
        alert('프로필 수정이 완료!!');
    } catch (error) {
        console.error("프로필 수정 중 오류 발생:", error);
        alert('프로필 수정 중 오류가 발생했습니다.');
    }
});

// 취소 버튼 클릭 시 이전 페이지로 이동
document.getElementById('cancel-button').addEventListener('click', () => {
    window.history.back();
});

// 프로필 버튼 클릭 시 페이지 이동 설정
document.getElementById('profile-button').addEventListener('click', () => {
    window.location.href = `user_pubprofile_update.html?username=${username}`;
});


// 페이지 로드 시 프로필 데이터 불러오기
getProfileDetailForUpdate();
