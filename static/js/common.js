
// 공통 Axios 설정
// 토큰, URL, 로그인

// Axios 기본 URL 설정
axios.defaults.baseURL = 'http://localhost:8000/api/';

// Authorization 헤더에 토큰 자동 추가
axios.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// 로그인 여부 확인, 리다이렉트
function checkSignin() {
    const token = localStorage.getItem('token');
    if (!token) {
        // 확인/취소 선택할 수 있는 알림창
        if (confirm('로그인이 필요합니다!\n로그인 페이지로 이동하시겠습니까?')) {
            location.href = 'user.html';
        }
        return false;
    }
    return true;
}


// navbar
fetch('../html/navbar.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('navbar').innerHTML = data;
    });

// footer
fetch('../html/footer.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('footer').innerHTML = data;
    });


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

    // Axios
    const axiosScript = document.createElement('script');
    axiosScript.src = 'https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js';
    body.appendChild(axiosScript);

    // Common JS
    const commonScript = document.createElement('script');
    commonScript.src = '../js/common.js';
    body.appendChild(commonScript);

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
});