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

// 회원 탈퇴 버튼 및 모달
const deleteAccountButton = document.getElementById('delete-account-button');
const deleteModal = document.getElementById('deleteModal');
const confirmDeleteButton = document.getElementById('confirm-delete-button');
const cancelDeleteButton = document.getElementById('cancel-delete-button');
const deletePasswordInput = document.getElementById('deletePassword');

// [계정 탈퇴] 버튼 클릭 시 모달 열기
if (deleteAccountButton) {
    deleteAccountButton.addEventListener('click', () => {
        deleteModal.style.display = 'block'; // 모달 표시
    });
}

// [모달 - 탈퇴 취소] 버튼 클릭 시 모달 닫기
if (cancelDeleteButton) {
    cancelDeleteButton.addEventListener('click', () => {
        deleteModal.style.display = 'none'; // 모달 닫기
    });
}

// [모달 - 탈퇴 확인] 버튼 클릭 시 탈퇴 요청 처리
if (confirmDeleteButton) {
    confirmDeleteButton.addEventListener('click', async () => {
        const deletePassword = deletePasswordInput.value; // 입력된 비밀번호 가져오기

        if (!deletePassword) {
            alert('비밀번호를 입력해주세요.');
            return;
        }

        // 회원 탈퇴 API 요청 보내기
        try {
            const response = await axios.post('user/withdraw/', {
                password: deletePassword
            });

            // 성공적으로 탈퇴되면 로그아웃 처리
            alert('계정이 삭제되었습니다. 로그아웃 처리 후 메인 페이지로 이동합니다.');
            localStorage.removeItem('token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('username');
            location.href = 'index.html'; // 메인 페이지로 이동

        } catch (error) {
            console.error('회원 탈퇴 중 오류 발생:', error);
            if (error.response && error.response.status === 400) {
                alert('비밀번호가 올바르지 않습니다.');
            } else {
                alert('서버에 문제가 발생했습니다. 나중에 다시 시도해주세요.');
            }
        } finally {
            deleteModal.style.display = 'none'; // 모달 닫기
        }
    });
}

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
