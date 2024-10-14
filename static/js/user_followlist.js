// URL에서 쿼리 파라미터로부터 username 추출하기
const urlParams = new URLSearchParams(window.location.search);
const username = urlParams.get('username');  // URL에 있는 'username' 파라미터 가져오기
//?username=aiden55 > 주소끝에 유저네임을 검색해야...

// username이 있으면 프로필 조회, 없으면 에러
if (username) {
    // 프로필 정보 가져오기
    async function getMyProfileData() {
        try {
            const response = await axios.get(`user/${username}/followinglist`);
            const data = response.data;

            // 프로필 정보 업데이트
            document.getElementById('my-nickname').innerText = data.nickname;
            document.getElementById('my-profile-image').src = data.profile_image || 'https://via.placeholder.com/100';
            document.getElementById('followers-count').innerText = `${data.follower_count} followers`;
            document.getElementById('following-count').innerText = `${data.following_count} following`;
        } catch (error) {
            console.error('프로필 정보를 가져오는 중 오류 발생:', error);
            alert('프로필 정보를 불러오는 중 오류가 발생했습니다.');
        }
    }

    // 팔로우 리스트 가져오기
    async function getFollowingList() {
        try {
            const response = await axios.get(`user/${username}/followinglist/`);
            const data = response.data;

            const followingList = document.getElementById('following-list');
            followingList.innerHTML = '';  // 기존 목록 초기화

            if (data.following_list.length === 0) {
                const noDataMessage = document.createElement('li');
                noDataMessage.innerText = '팔로우한 사용자가 없습니다.';
                followingList.appendChild(noDataMessage);
            } else {
                data.following_list.forEach(following => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `
                        <img src="${following.profile_image || 'https://via.placeholder.com/50'}" alt="User Profile" width="50" height="50">
                        <span>${following}</span>
                    `;
                    followingList.appendChild(listItem);
                });
            }
        } catch (error) {
            console.error('팔로우 목록을 가져오는 중 오류 발생:', error);
            alert('팔로우 목록을 불러오는 중 오류가 발생했습니다.');
        }
    }

    // 페이지 로드 시 데이터 가져오기
    document.addEventListener("DOMContentLoaded", function() {
        getMyProfileData();  // 프로필 정보
        getFollowingList();  // 팔로우한 사용자 목록
    });
} else {
    console.error('URL에서 사용자 이름을 찾을 수 없습니다.');
    alert('URL에서 사용자 이름을 찾을 수 없습니다.');
}
