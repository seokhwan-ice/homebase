// 팀 데이터 (팀 이름, 이미지 파일 이름, 팀 넘버 매핑)
const teams = [
    { name: "LG", logo: "5002.png", team_number: "5002" },
    { name: "KIA", logo: "2002.png", team_number: "2002" },
    { name: "롯데", logo: "3001.png", team_number: "3001" },
    { name: "한화", logo: "7002.png", team_number: "7002" },
    { name: "삼성", logo: "1001.png", team_number: "1001" },
    { name: "두산", logo: "6002.png", team_number: "6002" },
    { name: "SSG", logo: "9002.png", team_number: "9002" },
    { name: "NC", logo: "11001.png", team_number: "11001" },
    { name: "키움", logo: "10001.png", team_number: "10001" },
    { name: "KT", logo: "12001.png", team_number: "12001" }
];

// 팀 데이터를 HTML에 동적으로 추가하는 함수
function displayTeams() {
    const container = document.getElementById('team-container');

    // 각 팀 정보를 순회하며 HTML 구조 생성
    teams.forEach(team => {
        // 팀 카드 생성
        const teamCard = document.createElement('div');
        teamCard.classList.add('team-card');

        // 팀 카드에 링크 추가 (팀 넘버를 URL 쿼리 파라미터로 사용)
        const teamLink = document.createElement('a');
        teamLink.href = `data_team.html?team_number=${team.team_number}`;  // 팀 넘버를 쿼리 파라미터로 사용
        teamLink.classList.add('team-link');

        // 팀 로고 이미지 추가
        const teamLogo = document.createElement('img');
        teamLogo.src = `/static/images/${team.logo}`;  // 이미지 경로
        teamLogo.alt = `${team.name} 로고`;
        teamLink.appendChild(teamLogo); // 링크에 이미지 추가

        // 팀 이름 추가
        const teamName = document.createElement('p');
        teamName.textContent = team.name;
        teamLink.appendChild(teamName); // 링크에 팀 이름 추가

        // 팀 링크를 팀 카드에 추가
        teamCard.appendChild(teamLink);

        // 팀 카드를 컨테이너에 추가
        container.appendChild(teamCard);
    });
}

// 페이지 로딩 시 팀 데이터를 표시
window.onload = displayTeams;