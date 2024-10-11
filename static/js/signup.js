document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // 폼이 제출될 때 페이지 새로고침 방지

        // 폼 데이터 수집
        const formData = {
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
            name: document.getElementById('name').value,
            nickname: document.getElementById('nickname').value,  // 'nickname' 필드 추가
            email: document.getElementById('email').value,
            phone_number: document.getElementById('phone_number').value,
            bio: document.getElementById('bio').value
        };

        // Axios로 POST 요청 보내기
        axios.post('user/signup/', formData)  // 서버의 URL을 반드시 맞추세요
            .then(function (response) {
                // 요청이 성공하면
                alert('회원가입이 완료되었습니다!');
                console.log(response.data);

                // 회원가입이 성공하면 다른 페이지로 리다이렉트
                // 아래 코드를 나중에 다른 페이지가 준비되었을 때 활성화
                // location.href = 'home.html';  // 'home.html' 대신 실제 페이지 경로로 수정
            })
            .catch(function (error) {
                // 요청이 실패하면
                if (error.response) {
                    // 서버가 응답을 보냈지만, 응답 상태 코드가 2xx가 아닐 때
                    alert(`오류 발생: ${error.response.data.message}`);
                } else if (error.request) {
                    // 요청이 전송되었지만, 서버의 응답을 받지 못했을 때
                    alert('서버로부터 응답을 받지 못했습니다.');
                } else {
                    // 요청을 설정하는 과정에서 오류가 발생했을 때
                    alert('요청 중 오류가 발생했습니다.');
                }
                console.error('오류:', error);
            });
    });
});


