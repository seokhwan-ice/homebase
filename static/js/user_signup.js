document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('signup-form');

    // 프로필 이미지 미리보기 기능
    const profileImageInput = document.getElementById('profile_image');
    const profileImagePreview = document.createElement('img'); // 미리보기 이미지 태그 생성
    profileImagePreview.style.display = 'none'; // 기본적으로 안 보이게 설정
    profileImagePreview.width = 100; // 미리보기 이미지 크기 설정
    profileImageInput.after(profileImagePreview); // 이미지 업로드 필드 뒤에 미리보기 삽입

    // 이미지 선택 시 미리보기 업데이트
    profileImageInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                profileImagePreview.src = e.target.result; // 이미지 미리보기 설정
                profileImagePreview.style.display = 'block'; // 이미지를 화면에 표시
            };
            reader.readAsDataURL(file);
        }
    });

    // 폼 제출 이벤트
    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // 폼 제출 시 페이지 새로고침 방지

        // 비밀번호 일치 여부 확인
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (password !== confirmPassword) {
            alert('비밀번호와 비밀번호 확인이 일치하지 않습니다.');
            return; // 비밀번호가 일치하지 않으면 폼 제출 중단
        }

        // 입력한 데이터 수집
        const formData = new FormData();
        formData.append('username', document.getElementById('username').value);
        formData.append('name', document.getElementById('name').value);
        formData.append('nickname', document.getElementById('nickname').value);
        formData.append('email', document.getElementById('email').value); // 이메일 추가
        formData.append('password', password); // 확인된 비밀번호만 서버로 전송
        formData.append('phone_number', document.getElementById('phone_number')?.value || ''); // 선택 필드 (없을 수 있음)
        formData.append('bio', document.getElementById('bio')?.value || ''); // 선택 필드 (없을 수 있음)

        // 프로필 이미지가 있을 경우 추가
        const profileImage = profileImageInput.files[0];
        if (profileImage) {
            formData.append('profile_image', profileImage);
        }

        // formData 로그 출력 (디버깅용)
        console.log('Form data being sent:', formData);
        console.log('Password being sent:', formData.get('password'));
        try {
            // 서버로 데이터 전송
            const response = await axios.post('user/signup/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            // 응답 처리
            if (response.status === 201) {
                alert('회원가입 성공!');
                console.log('Server response status:', response.status); // 성공 시 응답 상태 코드 출력
                window.location.href = '../html/user_signin.html'; // 회원가입 성공 후 로그인 페이지로 리디렉션
            }
        } catch (error) {
            console.error('회원가입 중 오류 발생:', error);
            if (error.response) {
                alert(`오류 발생: ${error.response.data.message || error.response.data.detail || '알 수 없는 오류... 하...'}`);
            } else {
                alert('서버로부터 응답을 받지 못했습니다.');
            }
        }
    });
});

