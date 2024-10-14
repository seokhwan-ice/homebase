
// 직관인증게시판 글 목록 (live_list)

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

        // 이미지에 대한건 백엔드에서 수정할게요 디폴트 이미지 설정하는걸로
        const profileImage = live.author.profile_image ? `<img src="${live.author.profile_image}" alt="프로필 이미지" width="50">` : "이미지 없음";
        const liveImage = live.live_image ? `<img src="${live.live_image}" alt="게시글 이미지" width="100">` : "이미지 없음";

        liveItem.innerHTML = `
            <a href="live_detail.html?id=${live.id}">[${live.id}] ${live.home_team} vs ${live.away_team}</a>
            <br>경기장: ${live.stadium}
            <br>작성자: ${live.author.nickname} ${profileImage}
            <br>게시일: ${new Date(live.created_at).toLocaleString()}
            <br>${liveImage}
            <br>좋아요 수: ${live.likes_count}
            <br>댓글 수: ${live.comments_count}<hr>
        `;  // 이미지 추가, 작성일자 추가, 제목 수정
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