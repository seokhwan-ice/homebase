// API에서 선수 데이터를 가져오는 함수
async function fetchPlayersData(page = 1) {
    try {
        // 선수 데이터 API 호출
        const response = await axios.get(`data/players`); // URL 수정
        const players = response.data.results; // 페이지네이션에 따른 선수 목록
        const totalPages = response.data.total_pages; // 총 페이지 수

        // 데이터를 콘솔에 출력하여 확인
        console.log('선수 데이터:', players);

        const playersContainer = document.getElementById('players-container');
        playersContainer.innerHTML = ''; // 이전 내용 지우기
        const baseURL = 'https://statiz.sporki.com';

        // 선수 정보를 DOM에 추가
        players.forEach(player => {
            const playerDiv = document.createElement('div');
            playerDiv.className = 'player';

            // 이미지 URL 절대 경로로 변환
            const playerImage = `${baseURL}${player.profile_img}`; // 절대 경로로 변환

            // 이미지 URL 콘솔에 출력 (디버깅용)
            console.log('이미지 URL:', playerImage);

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
        displayPagination(page, totalPages);
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