
// 로그인 로그아웃 (테스트용)

const form = document.getElementById('signup-form');

form.addEventListener('submit', async function(event) {
    event.preventDefault();  // 기본 폼 제출 방지 (페이지 새로고침 방지)

    // html 파일에서 만든 form 데이터 가져와서 username, name, password변수에 저장
    const username = document.getElementById('username').value;
    const name = document.getElementById('name').value;
    const nickname = document.getElementById('nickname').value;
    const password = document.getElementById('password').value;
    // const confirm_password = document.getElementById('confirm_password').value;

    try {
        const response = await axios.post('user/signup/', {
            username: username,
            name: name,
            nickname: nickname, 
            password: password,
            // confirm_password: confirm_password
        });

        const data = response.data.access; 
        localStorage.setItem('data', data); // 로컬 스토리지에 저장하기
        alert('회원가입 성공!');

        // location.href =  'profile.html' // 메인페이지로 이동인데 일단 내 프로필 페이지로 이동하도록 경로 설정해둘게요

    } catch (error) {
        console.error("Error:", error);
        alert('회원가입 실패 다시 시도');
    }
});
