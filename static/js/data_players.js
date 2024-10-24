// 기존 팀 데이터 배열
const teams = [
    { name: "LG", logo: "5002.png" },
    { name: "KIA", logo: "2002.png" },
    { name: "롯데", logo: "3001.png" },
    { name: "한화", logo: "7002.png" },
    { name: "삼성", logo: "1001.png" },
    { name: "두산", logo: "6002.png" },
    { name: "SSG", logo: "9002.png" },
    { name: "NC", logo: "11001.png"},
    { name: "키움", logo: "10001.png"},
    { name: "KT", logo: "12001.png"}
];

// 페이지 로드 시 팀 로고를 상단에 표시
document.addEventListener('DOMContentLoaded', () => {
    const teamLogosContainer = document.getElementById('team-logos');

    // 모든 팀 로고를 상단에 추가
    teams.forEach(team => {
        const logo = document.createElement('img');
        logo.src = `/static/images/${team.logo}`;
        logo.alt = team.name;
        logo.style.width = '80px';
        logo.style.cursor = 'pointer';
        logo.addEventListener('click', () => {
            // 팀 이름을 쿼리 파라미터로 전달하여 선수 데이터 페이지로 이동
            window.location.href = `data_players.html?team_name=${encodeURIComponent(team.name)}`;
        });
        teamLogosContainer.appendChild(logo);
    });
});

// API에서 선수 데이터를 가져오는 함수
async function fetchPlayersData(page = 1) {
    const urlParams = new URLSearchParams(window.location.search); // URL에서 쿼리 파라미터 가져오기
    const teamName = urlParams.get('team_name'); // 팀 이름 가져오기

    try {
        // 팀 이름에 따른 선수 데이터 API 호출
        const response = await axios.get(`data/players?team_name=${encodeURIComponent(teamName)}`);
        const players = response.data.results; // 페이지네이션에 따른 선수 목록
        const totalPages = response.data.total_pages; // 총 페이지 수

        const playersContainer = document.getElementById('players-container');
        playersContainer.innerHTML = ''; // 이전 내용 지우기
        const baseURL = 'https://statiz.sporki.com';

        // 선수 목록을 팀 이름으로 필터링
        const filteredPlayers = players.filter(player => player.team_name === teamName);

        filteredPlayers.forEach(player => {
            const playerDiv = document.createElement('div');
            playerDiv.className = 'player';

            const playerImage = `${baseURL}${player.profile_img}`;
            if (player.profile_img) {
                playerDiv.innerHTML = `
                    <img src="${playerImage}" alt="${player.name} 프로필 이미지" onerror="this.onerror=null;" />
                    <h2 class="player-name" data-player-id="${player.id}" data-player-number="${player.player_number}">${player.name}</h2>
                    <p>팀: ${player.team_name}</p>
                `;
            } else {
                playerDiv.innerHTML = `
                    <h2 class="player-name" data-player-id="${player.id}" data-player-number="${player.player_number}">${player.name}</h2>
                    <p>팀: ${player.team_name}</p>
                `;
            }

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

// 페이지네이션을 표시하는 함수
function displayPagination(currentPage, totalPages) {
    const paginationContainer = document.getElementById('pagination-container');
    paginationContainer.innerHTML = ''; // 이전 내용 지우기

    for (let page = 1; page <= totalPages; page++) {
        const pageLink = document.createElement('a');
        pageLink.href = `?page=${page}`; // 페이지 링크 설정
        pageLink.textContent = page; // 링크 텍스트 설정

        if (page === currentPage) {
            pageLink.classList.add('active'); // 현재 페이지 강조
        }

        paginationContainer.appendChild(pageLink); // 페이지 링크를 페이지네이션 컨테이너에 추가
    }
}

// 페이지 로드 시 선수 데이터를 가져옴
window.onload = () => fetchPlayersData();