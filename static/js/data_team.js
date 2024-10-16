// API에서 팀 순위 데이터를 가져오는 함수
async function loadTeamRank() {
    try {
        const response = await axios.get('data/teamrank/');  // 팀 순위 데이터를 가져오는 API URL
        const data = response.data.results;  // 응답 데이터에서 팀 순위 목록을 가져옴 (pagination을 사용한다고 가정)

        const teamRankList = document.getElementById('team-rank');
        teamRankList.innerHTML = '';  // 기존 내용 초기화

        // 각 팀 순위 데이터를 리스트로 추가
        data.forEach(team => {
            const listItem = document.createElement('li');

            // 팀 이름을 클릭하면 상세 페이지로 이동하는 링크 생성
            const link = document.createElement('a');
            link.href = `/teamrank/${team.rank}/`;  // 팀 순위별 상세 페이지 URL로 설정
            link.textContent = `팀 순위 ${team.rank}: ${team.team_name}`;

            // 링크를 리스트 아이템에 추가
            listItem.appendChild(link);

            // 순위 정보를 팀 이름 옆에 추가
            const teamInfo = document.createElement('div');
            teamInfo.textContent = `
                경기 수: ${team.games_played}, 승: ${team.wins}, 패: ${team.losses}, 승률: ${team.win_rate}, 최근 10경기: ${team.last_10_games}
            `;

            // 리스트 아이템에 팀 정보를 추가
            listItem.appendChild(teamInfo);
            teamRankList.appendChild(listItem);
        });

    } catch (error) {
        console.error('팀 순위 데이터를 가져오는 중 오류 발생:', error);
        alert('팀 순위 데이터를 불러오는 중 오류가 발생했습니다.');
    }
}

// 페이지 로드 시 팀 순위 데이터를 가져옴
document.addEventListener('DOMContentLoaded', loadTeamRank);