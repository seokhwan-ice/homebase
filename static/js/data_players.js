// API에서 선수 데이터를 가져오는 함수
async function fetchPlayersData() {
  try {
    const response = await axios.get('data/players/');
    const players = response.data;

    // 데이터를 콘솔에 출력하여 확인
    console.log('선수 데이터:', players);  // 이 부분 추가

    const playersContainer = document.getElementById('players-container');

    // baseURL 설정
    const baseURL = 'https://statiz.sporki.com';

    players.forEach(player => {
      const playerDiv = document.createElement('div');
      playerDiv.className = 'player';

      // playerImage 변수 사용
      const playerImage = `${baseURL}${player.profile_img}`;  // 이미지 URL 수정

      playerDiv.innerHTML = `
        <img src="${playerImage}" alt="${player.name} 프로필 이미지" />
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
  } catch (error) {
    console.error('선수 데이터를 가져오는 중 오류 발생:', error);
  }
}

// 페이지 로드 시 선수 데이터를 가져옴
window.onload = fetchPlayersData;