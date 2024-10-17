// 로그인 로그아웃 (테스트용)
const form = document.getElementById('signin-form');
const logoutButton = document.getElementById('signout-button');  // 버튼 ID 오타 수정

form.addEventListener('submit', async function (event) {
    event.preventDefault();  // 기본 폼 제출 방지 (페이지 새로고침 방지)

    // html 파일에서 만든 form 데이터 가져와서 username, password 변수에 저장
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post('user/signin/', { // API 요청에 전체 URL 추가
            username: username,
            password: password
        });

        const accessToken = response.data.access;
        const refreshToken = response.data.refresh;

        localStorage.setItem('token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        localStorage.setItem('username', username);
        alert('로그인 성공!');

        location.href = '../html/index.html';  // 메인 페이지로 이동
        
    } catch (error) {
        console.error("Error:", error);
        alert('로그인 실패 다시 시도');
    }
});