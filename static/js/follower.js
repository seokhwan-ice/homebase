// Axios를 이용해 백엔드에서 나를 팔로우하는 사람 목록 가져오기
document.addEventListener('DOMContentLoaded', function() {
    const followersListElement = document.getElementById('followers-list');

    // 백엔드에서 팔로워 목록을 가져오는 API 엔드포인트
    const apiUrl = `/api/user/${username}/followerlist`; // 실제 API 엔드포인트로 변경

    axios.get(apiUrl)
        .then(response => {
            const followers = response.data;
            // 팔로워 목록 생성
            followers.forEach(follower => {
                const listItem = document.createElement('li');
                listItem.textContent = follower.username; // 팔로워의 사용자명
                followersListElement.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('팔로워 목록을 불러오는 중 오류 발생:', error);
        });
});
