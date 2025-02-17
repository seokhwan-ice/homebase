
// 공통 설정
// baseURL, 토큰 자동 추가, 로그인 여부 확인
// navbar, footer
// Bootstrap, FontAwesome, Google Fonts, Axios

// Axios 기본 URL 설정
if (location.hostname === 'home-base.co.kr') {
    axios.defaults.baseURL = 'https://home-base.co.kr/api/';  // 배포 환경
} else {
    axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';  // 로컬 환경
}

// Axios 요청 인터셉터: 헤더에 토큰 자동 추가
axios.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// Axios 응답 인터셉터: 토큰 만료 시 자동 로그아웃
axios.interceptors.response.use(response => {
    return response;
}, async error => {

    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;

        try {
            const response = await refreshAccessToken();

            const newAccessToken = response.data.access;
            if (newAccessToken) {
                localStorage.setItem('token', newAccessToken);
                originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
                return axios(originalRequest);
            }
        } catch (e) {
            alert('세션이 만료되었습니다. 다시 로그인해주세요.');
            localStorage.removeItem('token');
            localStorage.removeItem('refresh_token');
            location.href = 'user_signin.html';
        }
    }
    return Promise.reject(error);
});

// 토큰 갱신 함수
async function refreshAccessToken() {

    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
        location.href = 'user_signin.html';
        return Promise.reject("리프레시 토큰 없음");
    }

    try {
        const response = await axios.post('user/refresh/', {
            refresh: refreshToken
        });
        return response;
    } catch (error) {
        throw error;
    }
}

// 유저 활동 감지 (클릭, 키보드 누르기)
let userActive = false;
document.addEventListener('click', () => userActive = true);
document.addEventListener('keydown', () => userActive = true);

// 유저가 사용중이면 25분마다 토큰 갱신
setInterval(() => {
    if (userActive) {
        refreshAccessToken();
        userActive = false;
    }
}, 25 * 60 * 1000);


// 로그인 여부 확인, 리다이렉트 함수
function checkSignin() {
    const token = localStorage.getItem('token');
    if (!token) {
        if (confirm('로그인이 필요합니다!\n로그인 페이지로 이동하시겠습니까?')) {
            location.href = 'user_signin.html';
        }
        return false;
    }
    return true;
}


// head
function loadCommonHead() {
    const head = document.getElementsByTagName('head')[0];

    // Bootstrap CSS
    const bootstrapCSS = document.createElement('link');
    bootstrapCSS.rel = 'stylesheet';
    bootstrapCSS.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css';
    bootstrapCSS.integrity = 'sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH';
    bootstrapCSS.crossOrigin = 'anonymous';
    head.appendChild(bootstrapCSS);

    // Google Fonts
    const googleFonts1 = document.createElement('link');
    googleFonts1.rel = 'preconnect';
    googleFonts1.href = 'https://fonts.googleapis.com';
    head.appendChild(googleFonts1);

    const googleFonts2 = document.createElement('link');
    googleFonts2.rel = 'preconnect';
    googleFonts2.href = 'https://fonts.gstatic.com';
    googleFonts2.crossOrigin = 'anonymous';
    head.appendChild(googleFonts2);

    const fontStyle = document.createElement('link');
    fontStyle.rel = 'stylesheet';
    fontStyle.href = 'https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap';
    head.appendChild(fontStyle);

    // Common CSS
    const commonCSS = document.createElement('link');
    commonCSS.rel = 'stylesheet';
    commonCSS.href = '/static/css/common.css';
    head.appendChild(commonCSS);
}


// body
function loadCommonBody() {
    const body = document.getElementsByTagName('body')[0];

    // FontAwesome
    const fontAwesomeScript = document.createElement('script');
    fontAwesomeScript.src = 'https://kit.fontawesome.com/35728c8516.js';
    fontAwesomeScript.crossOrigin = 'anonymous';
    body.appendChild(fontAwesomeScript);

    // Bootstrap JS
    const bootstrapScript = document.createElement('script');
    bootstrapScript.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js';
    bootstrapScript.integrity = 'sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz';
    bootstrapScript.crossOrigin = 'anonymous';
    body.appendChild(bootstrapScript);
}

// DOM 로드 후 공통 요소 추가하기
document.addEventListener('DOMContentLoaded', () => {
    loadCommonHead();
    loadCommonBody();


    // navbar 로드 후 이벤트 리스너 등록
    fetch('/static/html/navbar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar').innerHTML = data;

            const token = localStorage.getItem('token');
            const signupButton = document.querySelector('a[href="user_signup.html"]');
            const signinButton = document.querySelector('a[href="user_signin.html"]');
            const signoutButton = document.getElementById('signout-link');
            const navbarUsername = document.getElementById('profile-link');
            const navbarProfileImg = document.getElementById('navbar-profile-img');
            const rightSidebar = document.querySelector('.sidebar-right');

            function handleSidebarAndButtons() {
                const username = localStorage.getItem('username');

                if (token) {
                    signupButton.style.display = 'none';
                    signinButton.style.display = 'none';
                    signoutButton.style.display = 'block';
                    navbarUsername.style.display = 'block';
                    navbarProfileImg.style.display = 'block';
                    rightSidebar.style.display = 'block';

                    if (username) {
                        // 모든 링크에 username 추가
                        document.querySelector('a[href="user_free_list.html"]').href = `user_free_list.html?username=${username}`;
                        document.querySelector('a[href="user_live_list.html"]').href = `user_live_list.html?username=${username}`;
                        document.querySelector('a[href="user_comment_list.html"]').href = `user_comment_list.html?username=${username}`;
                        document.querySelector('a[href="user_bookmark_list.html"]').href = `user_bookmark_list.html?username=${username}`;
                        document.querySelector('a[href="user_followerlist.html"]').href = `user_followerlist.html?username=${username}`;
                        document.querySelector('a[href="user_followlist.html"]').href = `user_followlist.html?username=${username}`;
                        const profileImage = localStorage.getItem('profile_image');
                        navbarUsername.textContent = username;
                        navbarProfileImg.src = profileImage && profileImage !== 'null'
                            ? profileImage.replace(/.*\/media/, '/media')
                            : 'https://i.imgur.com/CcSWvhq.png';

                    } else {
                        alert('로그인이 필요합니다.');
                        location.href = 'user_signin.html';
                    }
                } else {
                    signupButton.style.display = 'block';
                    signinButton.style.display = 'block';
                    signoutButton.style.display = 'none';
                    navbarUsername.style.display = 'none';
                    navbarProfileImg.style.display = 'none';
                    rightSidebar.style.display = 'none';
                }
            }

            handleSidebarAndButtons();
            window.addEventListener('resize', handleSidebarAndButtons);

            // [내프로필]
            if (navbarUsername) {
                navbarUsername.addEventListener('click', (event) => {
                    event.preventDefault();  // 기본 링크 동작 막기
                    const username = localStorage.getItem('username'); // localStorage에서 username 가져오기
                    if (username) {
                        location.href = `user_my_profile.html?username=${username}`; // username 파라미터 추가
                    } else {
                        alert('로그인이 필요합니다.');
                    }
                });
            }

            // [로그아웃]
            if (signoutButton) {
                signoutButton.addEventListener('click', async function (event) {
                    event.preventDefault();

                    // signout api 사용! 서버에 refresh token 줘서 blacklist 요청하기
                    const refreshToken = localStorage.getItem('refresh_token');
                    if (refreshToken) {
                        try {
                            await axios.post('user/signout/', { refresh: refreshToken });
                        } catch (error) {
                            alert('로그아웃 실패')
                        }
                    }

                    localStorage.removeItem('token');
                    localStorage.removeItem('refresh_token');
                    localStorage.removeItem('username');
                    alert('로그아웃 완료!!');
                    location.href = 'index.html';  // 로그인 후 메인페이지로
                });
            }
        })
        .catch(error => console.error('Navbar 로드 중에 발생한 오류임 -> common.js로 와라:', error));
    });


// footer
fetch('/static/html/footer.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('footer').innerHTML = data;
    });