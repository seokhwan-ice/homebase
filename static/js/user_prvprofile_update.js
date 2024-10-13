// URL에서 쿼리 파라미터로부터 username 추출하기
const params = new URLSearchParams(window.location.search);
const username = params.get('username');  // URL에 있는 'username' 파라미터 가져오기

if (!username) {
    alert('올바른 사용자를 찾을 수 없습니다.');
    throw new Error('username이 없습니다. 요청을 진행할 수 없습니다.');
}

// 전화번호 형식 확인 함수
const isValidPhoneNumber = (phoneNumber) => {
    const phonePattern = /^010-?[1-9]\d{3}-\d{4}$/;  // 서버의 RegexValidator와 일치하는 정규 표현식
    return phonePattern.test(phoneNumber);
};

// 프로필 데이터를 불러오기 (JWT 인증 필요 없음)
const getProfileDetailForUpdate = async () => {
    try {
        const response = await axios.get(`user/${username}/`);  // 프로필 데이터를 GET 요청으로 가져옴
        const profile = response.data;

        // 가져온 데이터를 폼에 반영 (기존 이메일 및 전화번호 표시)
        document.getElementById('current-email').value = profile.email;
        document.getElementById('current-phone_number').value = profile.phone_number;

    } catch (error) {
        console.error("프로필 데이터를 불러오는 중 오류 발생:", error);
        alert('프로필 데이터를 불러오는 중 오류가 발생했습니다.');
    }
};

// 비밀번호 수정 함수 추가 (비밀번호 필드가 둘 다 입력된 경우에만 요청)
const updatePassword = async () => {
    const oldPassword = document.getElementById('old-password').value;
    const newPassword = document.getElementById('new-password').value;

    // 두 비밀번호 필드가 모두 입력된 경우에만 수정 요청
    if (oldPassword && newPassword) {
        try {
            const response = await axios.put('user/password/', {
                old_password: oldPassword,
                new_password: newPassword
            }, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.status === 200) {
                alert('비밀번호가 성공적으로 변경되었습니다.');
            }
        } catch (error) {
            console.error("비밀번호 변경 중 오류 발생:", error);
            alert('비밀번호 변경 중 오류가 발생했습니다.');
        }
    } else if (oldPassword || newPassword) {
        // 하나만 입력된 경우 경고 메시지 표시
        throw new Error('비밀번호를 변경하려면 현재 비밀번호와 새 비밀번호를 모두 입력해야 합니다.');
    }
};

// 프로필 업데이트
const form = document.getElementById('account-form');
if (form) {
    form.addEventListener('submit', async function(event) {
        event.preventDefault();  // 폼 제출 방지

        const email = document.getElementById('email').value;
        const phone_number = document.getElementById('phone_number').value;

        const formData = {};

        // 이메일이 입력된 경우에만 추가
        if (email) {
            formData.email = email;
        }

        // 전화번호가 입력된 경우에만 추가
        if (phone_number) {
            if (!isValidPhoneNumber(phone_number)) {
                alert('전화번호 형식이 올바르지 않습니다. 010-XXXX-XXXX 형식으로 입력하세요.');
                return;  // 잘못된 전화번호 형식인 경우 더 이상 진행하지 않음
            }
            formData.phone_number = phone_number;
        }

        try {
            // 비밀번호 필드 확인 및 수정 요청 (비밀번호가 올바르지 않으면 throw로 여기서 중단됨)
            await updatePassword();

            // 프로필 정보 수정
            const profileResponse = await axios.patch(`user/${username}/`, formData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (profileResponse.status === 200) {
                // 수정 성공 시 확인 메시지 표시
                alert('프로필 수정이 완료되었습니다.');
            } else {
                alert('프로필 수정 중 오류가 발생했습니다.');
            }

        } catch (error) {
            console.error("프로필 수정 중 오류 발생:", error);
            alert('프로필 수정 중 오류가 발생했습니다.');
        }
    });
}

// 취소 버튼 클릭 시 이전 페이지로 이동
document.getElementById('cancel-button').addEventListener('click', function() {
    if (document.referrer) {
        window.history.back();  // 이전 페이지로 이동
    } else {
        location.href = 'home.html';  // 이전 페이지가 없을 경우 홈 페이지로 이동
    }
});

// 페이지 로드 시 프로필 데이터 불러오기
getProfileDetailForUpdate();

// 프로필 버튼 클릭 시 사용자 이름에 따라 동적 페이지 이동
document.getElementById('profile-button').addEventListener('click', function() {
    location.href = `public_profile_update.html?username=${username}`;
});
