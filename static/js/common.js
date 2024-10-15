
// 공통 설정
// baseURL, 토큰 자동 추가, 로그인 여부 확인
// navbar, footer
// Bootstrap, FontAwesome, Google Fonts, Axios

// Axios 기본 URL 설정
axios.defaults.baseURL = 'http://localhost:8000/api/';

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
    console.log("401 에러 발생. 응답 인터셉터 작동 중.");

    if (error.response && error.response.status === 401) {
        try {
            console.log("401 에러 -> 토큰 갱신 시도 중.");

            const response = await refreshAccessToken();

            const newAccessToken = response.data.access;
            if (newAccessToken) {
                console.log("토큰 갱신 성공. 새로운 액세스 토큰:", newAccessToken);
                localStorage.setItem('token', newAccessToken);
                error.config.headers['Authorization'] = `Bearer ${newAccessToken}`;
                return axios(error.config);
            }
        } catch (e) {
            console.error("토큰 갱신 실패. 에러:", e);
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
    console.log("refreshAccessToken 함수 호출은 되고 있는거니");

    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
        console.error("리프레시 토큰 없음. 로그인 페이지로 이동함.");
        location.href = 'user_signin.html';
        return Promise.reject("리프레시 토큰 없음");
    }

    try {
        console.log("리프레시 토큰으로 토큰 갱신 시도 중.");
        const response = await axios.post('user/refresh/', {
            refresh: refreshToken
        });

        console.log("토큰 갱신 성공. 응답:", response.data);
        return response;
    } catch (error) {
        console.error("토근 갱신 실패. 에러:", error);
        throw error;
    }
}

// 유저 활동 감지 (클릭, 키보드 누르기)
let userActive = false;
document.addEventListener('click', () => userActive = true);
document.addEventListener('keydown', () => userActive = true);

// 유저가 사용중이면 25분마다 토큰 갱신
setInterval(() => {
    console.log("20초 지났다. userActive 상태:", userActive);

    if (userActive) {
        refreshAccessToken();
        userActive = false;
    }
}, 20 * 1000);


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
    commonCSS.href = '../css/common.css';
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
    fetch('../html/navbar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar').innerHTML = data;

            // [내프로필] 버튼 클릭 이벤트 리스너 추가
            const profileLink = document.getElementById('profile-link');
            if (profileLink) {  // 버튼이 존재하는지 확인  >>> 로그인 여부에 따라 버튼 다르게 보이게 하쟈
                profileLink.addEventListener('click', (event) => {
                    event.preventDefault();  // 기본 링크 동작 막기
                    const username = localStorage.getItem('username'); // localStorage에서 username 가져오기
                    if (username) {
                        location.href = `user_my_profile.html?username=${username}`; // username 파라미터 추가
                    } else {
                        alert('로그인이 필요합니다.');  // >>> 로그인 여부에 따라 버튼 다르게 보이게 하쟈
                    }
                });
            }

            // [로그아웃] 버튼 클릭 이벤트 리스너 추가
            const signoutButton = document.getElementById('signout-link');
            if(signoutButton) {
                signoutButton.addEventListener('click', function (event) {
                    event.preventDefault();  // 기본 링크 동작 막기
                    localStorage.removeItem('token');
                    localStorage.removeItem('refresh_token');
                    localStorage.removeItem('username');
                    alert('로그아웃 완료!!');
                    location.href = '../html/index.html';  // 로그인 후 메인페이지로
                });
            }
        })
        .catch(error => console.error('Navbar 로드 중에 발생한 오류임 -> common.js로 와라:', error));
    });


// footer
fetch('../html/footer.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('footer').innerHTML = data;
    });