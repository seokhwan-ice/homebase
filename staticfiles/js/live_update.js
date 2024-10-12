
// 직관인증게시판 글 수정 (live_update)

const params = new URLSearchParams(location.search);
const liveId = params.get('id');

const getLiveDetailForUpdate = async () => {
    try {
        const response = await axios.get(`community/live/${liveId}/`);
        const live = response.data;

        document.getElementById('home_team').value = live.home_team;
        document.getElementById('away_team').value = live.away_team;
        document.getElementById('stadium').value = live.stadium;
        // 날짜는 초기화 돼서 표시되네.... 할수 있으면 덮어씌우기
        document.getElementById('game_date').value = live.game_date;
        document.getElementById('seat').value = live.seat || "";
        document.getElementById('review').value = live.review;

    } catch (error) {
        console.error("Error:", error);
        alert("글 불러오기 실패");
    }
};

getLiveDetailForUpdate();

const form = document.getElementById('update-form');
form.addEventListener('submit', async function(event) {
    event.preventDefault();

    if (!checkSignin()) return;

    const formData = new FormData(form);
    try {
        await axios.put(`community/live/${liveId}/`, formData);
        alert('글 수정 완료!');
        location.href = `live_detail.html?id=${liveId}`;  // 상세 페이지 이동
    } catch (error) {
        console.error("Error:", error);
        alert('글 수정 실패');
    }
});