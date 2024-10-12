document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // 폼이 제출될 때 페이지 새로고침 방지

        // 폼 데이터 수집
        const formData = new FormData();
        formData.append('username', document.getElementById('username').value);
        formData.append('password', document.getElementById('password').value);
        formData.append('name', document.getElementById('name').value);
        formData.append('nickname', document.getElementById('nickname').value);
        formData.append('email', document.getElementById('email').value);
        formData.append('phone_number', document.getElementById('phone_number').value);
        formData.append('bio', document.getElementById('bio').value);

        const profileImage = document.getElementById('profile_image').files[0];
        if (profileImage) {
            formData.append('profile_image', profileImage);
        }

        // Axios로 POST 요청 보내기
        axios.post('http://127.0.0.1:8000/api/user/signup/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(function(response) {
            alert('회원가입 성공!!!!');
            console.log(response.data);
        })
        .catch(function(error) {
            if (error.response) {
                alert(`오류 발생: ${error.response.data.message}`);
            } else if (error.request) {
                alert('서버로부터 응답을 받지 못했습니다.');
            } else {
                alert('요청 중 오류가 발생했습니다.');
            }
            console.error('오류:', error);
        });
    });

    // 취소 버튼 클릭 시 뒤로가기
    document.querySelector('button[type="reset"]').addEventListener('click', function(event) {
        event.preventDefault();  // 기본 취소 동작을 막음
        window.history.back();    // 이전 페이지로 이동
    });
});

