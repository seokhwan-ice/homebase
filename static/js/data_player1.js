let currentPlayersPage = 1;  // 현재 선수 페이지
let totalPlayersPages = 0;    // 총 선수 페이지 수
let currentRecordsPage = 1;    // 현재 선수 기록 페이지
let totalRecordsPages = 0;      // 총 선수 기록 페이지 수

// API에서 선수 데이터를 가져오는 함수
async function fetchPlayersData(page = 1) {
    try {
        const response = await axios.get(`data/players`); // URL 수정
        const players = response.data.results; // 페이지네이션에 따른 선수 목록
        totalPlayersPages = response.data.total_pages; // 총 페이지 수

        const playersContainer = document.getElementById('players-container');
        playersContainer.innerHTML = ''; // 이전 내용 지우기
        const baseURL = 'https://statiz.sporki.com';

        // 선수 정보를 DOM에 추가
        players.forEach(player => {
            const playerDiv = document.createElement('div');
            playerDiv.className = 'player';

            // 이미지 URL 절대 경로로 변환
            const playerImage = `${baseURL}${player.profile_img}`; // 절대 경로로 변환

            // 선수 정보 표시
            playerDiv.innerHTML = `
                <img src="${playerImage}" alt="${player.name} 프로필 이미지" onerror="this.onerror=null; this.src='path/to/default-image.jpg';" />
                <h2>${player.name}</h2>
                <p>팀: ${player.team}</p>
                <p>포지션: ${player.position}</p>
                <p>타격손: ${player.batter_hand}</p>
                <p>생년월일: ${player.birth_date ? player.birth_date : '정보 없음'}</p>
                <p>출신학교: ${player.school ? player.school : '정보 없음'}</p>
                <p>신인지명: ${player.draft_info ? player.draft_info : '정보 없음'}</p>
                <p>활약연도: ${player.active_years ? player.active_years : '정보 없음'}</p>
                <p>활약팀: ${player.active_team ? player.active_team : '정보 없음'}</p>
            `;

            playersContainer.appendChild(playerDiv);
        });

        // 페이지네이션 표시
        displayPlayersPagination(currentPlayersPage, totalPlayersPages);
    } catch (error) {
        console.error('선수 데이터를 가져오는 중 오류 발생:', error);
    }
}

// 선수 기록을 가져오는 함수
function fetchPlayerRecords(page = 1) {
    axios.get(`data/players_rival/?page=${page}`) // API URL 확인
        .then(response => {
            const playerRecords = response.data.results;  // 페이지네이션 결과
            totalRecordsPages = response.data.total_pages; // 총 페이지 수
            const tableBody = document.querySelector("#player-records-table tbody");
            tableBody.innerHTML = '';  // 기존 데이터 지우기

            playerRecords.forEach(record => {
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
                    cell.textContent = record[field];
                    row.appendChild(cell);
                });

                tableBody.appendChild(row);
            });

            updateRecordsPaginationButtons();
        })
        .catch(error => {
            console.error("데이터를 가져오는 중 오류 발생:", error);
        });
}

// 선수 페이지네이션 표시 함수
function displayPlayersPagination(currentPage, totalPages) {
    const paginationContainer = document.getElementById('pagination-container');
    paginationContainer.innerHTML = ''; // 이전 내용 지우기

    for (let i = 1; i <= totalPages; i++) {
        const pageLink = document.createElement('a');
        pageLink.innerText = i;
        pageLink.href = '#';
        pageLink.onclick = () => {
            currentPlayersPage = i;
            fetchPlayersData(i); // 클릭 시 해당 페이지 데이터 가져오기
        };

        if (i === currentPage) {
            pageLink.className = 'active'; // 현재 페이지 표시
        }

        paginationContainer.appendChild(pageLink);
    }
}

// 선수 기록 페이지 전환 함수
function changeRecordsPage(direction) {
    currentRecordsPage += direction;
    fetchPlayerRecords(currentRecordsPage);
}

// 선수 기록 페이지네이션 버튼 업데이트 함수
function updateRecordsPaginationButtons() {
    const prevButton = document.getElementById("prev-page");
    const nextButton = document.getElementById("next-page");

    prevButton.disabled = currentRecordsPage === 1;
    nextButton.disabled = currentRecordsPage === totalRecordsPages;
}

// 페이지가 로드될 때 선수 데이터와 기록을 가져오기
document.addEventListener("DOMContentLoaded", () => {
    fetchPlayersData(currentPlayersPage); // 선수 데이터 가져오기
    fetchPlayerRecords(currentRecordsPage); // 선수 기록 가져오기
});