// 기본 URL 설정
const baseURL = 'https://statiz.sporki.com'; // Django 서버의 기본 URL

async function fetchPlayerData() {
    const urlParams = new URLSearchParams(window.location.search); // URL에서 쿼리 파라미터 가져오기
    const player_Number = parseInt(urlParams.get('player_number'), 10); // player_number를 정수로 변환

    console.log('선수 번호:', player_Number); // 선수 번호 확인

    // player_Number가 유효한지 검사
    if (isNaN(player_Number)) {
        console.error('유효하지 않은 선수 번호입니다.'); // 오류 메시지 로그
        return; // 함수 종료
    }

    try {
        // 1. 선수 기본 정보 가져오기 (DB에서)
        const playerInfoResponse = await axios.get(`data/players/${player_Number}/`); // 선수 기본 정보 API 호출
        const playerInfo = playerInfoResponse.data; // 응답 데이터

        console.log('선수 기본 정보:', playerInfo); // 선수 기본 정보 확인

        // 2. 선수 라이벌 기록 가져오기
        const playerRivalResponse = await axios.get(`data/players_rival/${player_Number}/`); // 선수 라이벌 기록 API 호출
        const playerRivalRecords = playerRivalResponse.data; // 응답 데이터

        console.log('선수 라이벌 기록:', playerRivalRecords); // 선수 라이벌 기록 확인

        // 선수 정보 표시하는 코드 추가
        const playerInfoSection = document.querySelector("#player-info-section");
        const playerImage = `${baseURL}${playerInfo.profile_img || '/path/to/default-image.jpg'}`; // 이미지 URL 절대 경로로 변환
        playerInfoSection.innerHTML = `
            <img src="${playerImage}" alt="프로필 이미지">
            <h3>${playerInfo.name}</h3>
            <p>팀: ${playerInfo.team_name || '-'}</p>
            <p>포지션: ${playerInfo.position || '-'}</p>
            <p>타격 손: ${playerInfo.batter_hand || '-'}</p>
            <p>출생일: ${playerInfo.birth_date || '-'}</p>
            <p>학교: ${playerInfo.school || '-'}</p>
            <p>드래프트 정보: ${playerInfo.draft_info || '-'}</p>
            <p>활동 기간: ${playerInfo.active_years || '-'}</p>
            <p>현재 팀: ${playerInfo.active_team || '-'}</p>
        `;

        // 테이블에 선수 라이벌 기록 추가
        const tableBody = document.querySelector("#player-records-table tbody");
        tableBody.innerHTML = ''; // 기존 내용 지우기

        // playerRivalRecords가 배열인지 확인
        if (Array.isArray(playerRivalRecords)) {
            playerRivalRecords.forEach(record => {
                const row = document.createElement('tr');

                // 나머지 필드 추가
                const fields = [
                    'name', 'opponent', 'pa', 'epa', 'ab', 'r', 'h',
                    'two_b', 'three_b', 'hr', 'tb', 'rbi', 'bb', 'hp',
                    'ib', 'so', 'gdp', 'sh', 'sf', 'avg', 'obp', 'slg',
                    'ops', 'np', 'avli', 're24', 'wpa'
                ];

                fields.forEach(field => {
                    const cell = document.createElement('td');
                    cell.textContent = record[field] !== undefined ? record[field] : '-'; // 값이 없을 경우 '-'
                    row.appendChild(cell);
                });

                tableBody.appendChild(row);
            });
        } else {
            console.error('playerRivalRecords는 배열이 아닙니다.', playerRivalRecords);
        }

    } catch (error) {
        console.error('선수 정보를 가져오는 중 오류 발생:', error.response ? error.response.data : error.message);
    }
}

// 페이지가 로드될 때 선수 데이터 가져오기
window.onload = () => {
    console.log('현재 URL:', window.location.href); // 현재 URL 로그
    fetchPlayerData(); // 선수 데이터 로드
};