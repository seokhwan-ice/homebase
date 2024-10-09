
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
        alert('로그인이 필요합니다!');
        location.href = 'user.html';  // 이동할 페이지
        return false;
    }
    return true;
}