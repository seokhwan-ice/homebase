
// 직관인증게시판 글 목록 (live_list)

const getLiveList = async (query = '') => {
    try {
        const response = await axios.get(`community/live/?q=${query}`);
        const data = response.data;

        const liveList = document.getElementById('live-list');
        liveList.innerHTML = '';  // 기존 목록 초기화

        data.forEach(live => {
            const liveListItem = document.createElement('li');

            // 이미지에 대한건 백엔드에서 수정할게요 디폴트 이미지 설정하는걸로
            const profileImage = live.author.profile_image ? `<img src="${live.author.profile_image}" alt="프로필 이미지" width="50">` : "이미지 없음";
            const liveImage = live.live_image ? `<img src="${live.live_image}" alt="게시글 이미지" width="100">` : "이미지 없음";

            liveListItem.innerHTML = `
                <a href="live_detail.html?id=${live.id}">[${live.id}] ${live.home_team} vs ${live.away_team}</a>
                <br>경기장: ${live.stadium}
                <br>작성자: ${live.author.nickname} ${profileImage}
                <br>게시일: ${new Date(live.created_at).toLocaleString()}
                <br>${liveImage}
                <br>좋아요 수: ${live.likes_count}
                <br>댓글 수: ${live.comments_count}<hr>
            `;  // 이미지 추가, 작성일자 추가, 제목 수정
            liveList.appendChild(liveListItem);
        });
    } catch (error) {
        console.error("Error:", error);
        alert("글 목록 불러오기 실패");
    }
};

getLiveList();

// 필터링 검색 기능 추가해야됨