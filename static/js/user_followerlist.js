// 팔로우 리스트 가져오기
async function getfollowersList() {
    try {
        const followersList = document.getElementById('followers-list');
        if (!followersList) {
            console.error('followers-list 요소를 찾을 수 없습니다.');
            return;
        }
        
        const response = await axios.get(`user/${username}/followerslist/`);
        const data = response.data;

        followersList.innerHTML = '';  // 기존 목록 초기화

        if (data.followers_list.length === 0) {
            const noDataMessage = document.createElement('li');
            noDataMessage.innerText = '팔로우한 사용자가 없습니다.';
            followersList.appendChild(noDataMessage);
        } else {
            data.followers_list.forEach(followers => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <img src="${followers.profile_image || 'https://via.placeholder.com/50'}" alt="User Profile" width="50" height="50">
                    <span>${followers}</span>
                `;
                followersList.appendChild(listItem);
            });
        }
    } catch (error) {
        console.error('팔로우 목록을 가져오는 중 오류 발생:', error);
        alert('팔로우 목록을 불러오는 중 오류가 발생했습니다.');
    }
}




// 프로필 페이지 완성 후 팔로우 사람의 닉네임을 클릭하면 해당유저의 프로필로 이동 만들어야해요