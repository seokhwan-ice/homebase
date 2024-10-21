
const filterSearch = document.getElementById('filter-search');
const sortSearch = document.getElementById('sort-search');

// 필터링 검색 함수
const getFilteredLiveList = async () => {
    try {
        let url = 'community/live/?';
        const gameDate = document.getElementById('game-date').value;
        const stadium = document.getElementById('stadium').value;
        const team = document.getElementById('team').value;
        const sort = sortSearch.value;

        if (gameDate) url += `game_date=${gameDate}&`;
        if (stadium) url += `stadium=${stadium}&`;
        if (team) url += `team=${team}&`;
        if (sort) url += `sort=${sort}`;

        const response = await axios.get(url);
        const data = response.data;

        renderLiveList(data);

    } catch (error) {
        console.error('Error:', error);  // test
        alert('목록 가져오기 실패')  // test
    }
};

// 글 목록 렌더링 함수
const renderLiveList = (liveList) => {
    const liveListContainer = document.getElementById('live-list');
    liveListContainer.innerHTML = '';

    liveList.forEach(live => {
        const liveItem = document.createElement('li');

        // profile_image
        const profileImage = document.createElement('img');
        if (live.author.profile_image) {
            const profileImageUrl = live.author.profile_image.split(',');
            const cleanProfileImage = profileImageUrl[0] + profileImageUrl[1].substring(profileImageUrl[1].indexOf('/'));
            profileImage.src = cleanProfileImage;
        } else {
            profileImage.src = 'https://i.imgur.com/CcSWvhq.png';
        }
        profileImage.alt = '프로필 이미지';
        profileImage.classList.add('profile-image');  // clas 지정

        // live_image
        const liveImage = document.createElement('img');
        const liveImageUrl = live.live_image.split(',');
        const cleanLiveImage = liveImageUrl[0] + liveImageUrl[1].substring(liveImageUrl[1].indexOf('/'));
        liveImage.src = cleanLiveImage;
        liveImage.alt = '게시글 이미지';
        liveImage.classList.add('live-image');  // class 지정
        
        const formattedDate = new Date(live.created_at).toLocaleDateString('ko-KR', { month: '2-digit', day: '2-digit' });

        liveItem.innerHTML = `
            <a href="live_detail.html?id=${live.id}" class="card-link">
                <div class="profile-section">
                    <div class="author">
                        ${profileImage.outerHTML}
                        <span class="nickname">${live.author.nickname}</span>
                    </div>
                    <span class="date">${formattedDate}</span>
                </div>
                ${liveImage.outerHTML}
                <div class="info">
                    <h2>${live.home_team} vs ${live.away_team}</h2>
                    <div class="meta">
                        <p class="stadium">${live.stadium}</p>
                        <div class="icon-container">
                            <span><i class="fa-solid fa-heart"></i> ${live.likes_count}</span>
                            <span><i class="fa-solid fa-comment"></i> ${live.comments_count}</span>
                        </div>
                    </div>
                </div>
            </a>
        `;
        liveListContainer.appendChild(liveItem);
    });
};

// 필터 검색 이벤트
filterSearch.addEventListener('submit', function(event) {
    event.preventDefault();
    getFilteredLiveList()
});

// 정렬 검색 이벤트
sortSearch.addEventListener('change', function() {
    getFilteredLiveList();
});

getFilteredLiveList();