let currentPage = 1;  // 현재 페이지
let totalPages = 0;   // 총 페이지 수
let currentPlayerId;  // 현재 선수 ID 저장

    // API에서 선수 데이터를 가져오는 함수
async function fetchPlayersData() {
    try {
        const response = await axios.get('data/players/');
        const players = response.data;

            // 선수 데이터 출력
        const playersContainer = document.getElementById('players-container');
        const baseURL = 'https://statiz.sporki.com';

        players.forEach(player => {
            const playerDiv = document.createElement('div');
            playerDiv.className = 'player';

            const playerImage = `${baseURL}${player.profile_img}`;

            playerDiv.innerHTML = `
                <img src="${playerImage}" alt="${player.name} 프로필 이미지" />
                <p>이름: ${player.name}</p>
                <p>팀: ${player.team}</p>
                <p>포지션: ${player.position}</p>
                <p>타격손: ${player.batter_hand}</p>
                <p>생년월일: ${player.birth_date ? player.birth_date : '정보 없음'}</p>
                <p>출신학교: ${player.school ? player.school : '정보 없음'}</p>
                <p>신인지명: ${player.draft_info ? player.draft_info : '정보 없음'}</p>
                <p>활약연도: ${player.active_years ? player.active_years : '정보 없음'}</p>
                <p>활약팀: ${player.active_team ? player.active_team : '정보 없음'}</p>
                <button onclick="fetchPlayerRecords(${player.id})">상대 전적 보기</button>
            `;

            playersContainer.appendChild(playerDiv);
        });
    } catch (error) {
        console.error('선수 데이터를 가져오는 중 오류 발생:', error);
    }
}

    // 특정 선수의 상대 전적을 가져오는 함수
function fetchPlayerRecords(playerId, page = 1) {
    currentPlayerId = playerId; // 현재 선수 ID 설정
    axios.get(`data/players_rival/?player_id=${playerId}&page=${page}`)
        .then(response => {
            const playerRecords = response.data.results;
            totalPages = response.data.total_pages;
            const tableBody = document.querySelector("#player-records-table tbody");
            tableBody.innerHTML = ''; // 기존 데이터 지우기

            playerRecords.forEach(record => {
                const row = document.createElement('tr');

                const logoCell = document.createElement('td');
                const logoImg = document.createElement('img');
                logoImg.src = record.team_logo_url; // 팀 로고 URL
                logoImg.alt = `${record.opponent}의 팀 로고`;
                logoCell.appendChild(logoImg);
                row.appendChild(logoCell);

                const fields = [
                    'opponent', 'pa', 'epa', 'ab', 'r', 'h',
                    'two_b', 'three_b', 'hr', 'tb', 'rbi', 'bb', 'hp',
                    'ib', 'so', 'gdp', 'sh', 'sf', 'avg', 'obp', 'slg',
                    'ops', 'np', 'avli', 're24', 'wpa'
                ];
                fields.forEach(field => {
                    const cell = document.createElement('td');
                    cell.textContent = record[field];
                    row.appendChild(cell);
                });

                tableBody.appendChild(row);
            });

            updatePaginationButtons();
        })
        .catch(error => {
            console.error("데이터를 가져오는 중 오류 발생:", error);
        });
}

    // 페이지를 변경하는 함수
function changePage(direction) {
    currentPage += direction;
    fetchPlayerRecords(currentPlayerId, currentPage); // currentPlayerId는 현재 선수의 ID입니다.
}

    // 페이지네이션 버튼 상태 업데이트
function updatePaginationButtons() {
    const prevButton = document.getElementById("prev-page");
    const nextButton = document.getElementById("next-page");

    prevButton.disabled = currentPage === 1;
    nextButton.disabled = currentPage === totalPages;
}

    // 페이지 로드 시 선수 데이터를 가져옴
window.onload = fetchPlayersData;
