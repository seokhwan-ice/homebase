// API에서 선수 데이터를 가져오는 함수
async function fetchPlayersData(page = 1) {
    try {
        const response = await axios.get(`data/players`); // 선수 데이터 API 호출
        const players = response.data.results; // 페이지네이션에 따른 선수 목록
        const totalPages = response.data.total_pages; // 총 페이지 수

        const playersContainer = document.getElementById('players-container');
        playersContainer.innerHTML = ''; // 이전 내용 지우기
        const baseURL = 'https://statiz.sporki.com';

        players.forEach(player => {
            const playerDiv = document.createElement('div');
            playerDiv.className = 'player';

            // 이미지 URL 절대 경로로 변환
            const playerImage = `${baseURL}${player.profile_img}`;

            // 선수 정보 표시 (player_number 추가)
            playerDiv.innerHTML = `
                <img src="${playerImage}" alt="${player.name} 프로필 이미지" onerror="this.onerror=null; this.src='path/to/default-image.jpg';" />
                <h2 class="player-name" data-player-id="${player.id}" data-player-number="${player.player_number}">${player.name}</h2>
                <p>팀: ${player.team}</p>
            `;

            playersContainer.appendChild(playerDiv);
        });

        // 페이지네이션 표시
        displayPagination(page, totalPages);

        // 선수 이름 클릭 이벤트 추가
        const playerNames = document.querySelectorAll('.player-name');
        playerNames.forEach(name => {
            name.addEventListener('click', function () {
                const playerNumber = this.dataset.playerNumber; // player_number 가져오기
                console.log('클릭한 선수 번호:', playerNumber); // 선수 번호 확인
                window.location.href = `data_player_rival.html?player_number=${playerNumber}`; // 상세 페이지로 이동
            });
        });
    } catch (error) {
        console.error('선수 데이터를 가져오는 중 오류 발생:', error);
    }
}

// 페이지네이션 표시 함수
function displayPagination(currentPage, totalPages) {
    const paginationContainer = document.getElementById('pagination-container');
    paginationContainer.innerHTML = ''; // 이전 내용 지우기

    for (let i = 1; i <= totalPages; i++) {
        const pageLink = document.createElement('a');
        pageLink.innerText = i;
        pageLink.href = '#';
        pageLink.onclick = () => {
            fetchPlayersData(i); // 클릭 시 해당 페이지 데이터 가져오기
        };

        if (i === currentPage) {
            pageLink.className = 'active'; // 현재 페이지 표시
        }

        paginationContainer.appendChild(pageLink);
    }
}

// 페이지 로드 시 선수 데이터를 가져옴
window.onload = () => fetchPlayersData();