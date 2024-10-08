
// 공통 Axios 설정
// 토큰, URL

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