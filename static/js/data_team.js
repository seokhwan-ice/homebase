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

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const teamNumber = urlParams.get('team_number');

    if (teamNumber) {
        fetchTeamData(teamNumber);
    } else {
        alert('팀 번호가 없습니다.');
    }
});

function fetchTeamData(teamNumber) {
    if (!teamNumber) {
        alert('팀 번호를 입력해 주세요.');
        return;
    }

    Promise.all([
        fetchTeamRank(teamNumber),
        fetchTeamRivalRecords(teamNumber),
        fetchTeamDetails(teamNumber)
    ]).then((responses) => {
        const [rankData, rivalData, detailData] = responses;

        displayTeamRank(rankData);
        displayRivalRecords(rivalData);
        displayTeamDetails(detailData);
    }).catch(error => {
        console.error('데이터 가져오기 오류:', error);
    });
}

function fetchTeamRank(teamNumber) {
    return axios.get(`data/teamrank/${teamNumber}/`).then(response => {
        const data = response.data;
        return {
            ...data,
            logo_url: `/static/images/team_logo_${teamNumber}.png`,
            team_name: data.team_name // API에서 팀 이름 가져오기
        };
    });
}

function fetchTeamRivalRecords(teamNumber) {
    return axios.get(`data/teamrival/${teamNumber}/`).then(response => response.data);
}

function fetchTeamDetails(teamNumber) {
    return axios.get(`data/teamdetail/${teamNumber}/`).then(response => response.data);
}

function displayTeamRank(rankData) {
    const rankDiv = document.getElementById('team-rank');
    const teamLogo = document.getElementById('team-logo');
    const teamName = document.getElementById('team-name');

    // 팀 로고와 팀 이름 설정
    const team = teams.find(t => t.logo === `${rankData.team_number}.png`);
    if (team) {
        teamLogo.src = `/static/images/${team.logo}`; // 로고 경로 설정
        teamName.innerText = team.name; // 팀 이름 설정
    } else {
        teamLogo.src = `/static/images/default_logo.png`; // 기본 로고
        teamName.innerText = "알 수 없는 팀"; // 기본 팀 이름
    }

    rankDiv.innerHTML = `
        <h2>팀 순위</h2>
        <p>순위: ${rankData.rank}</p>
        <p>경기 수: ${rankData.games_played}</p>
        <p>승: ${rankData.wins}</p>
        <p>무: ${rankData.draws}</p>
        <p>패: ${rankData.losses}</p>
        <p>승률: ${rankData.win_rate}</p>
        <p>최근 10경기 성적: ${rankData.last_10_games}</p>
        <p>연속 성적: ${rankData.streak}</p>
    `;
}

function displayRivalRecords(rivalData) {
    const rivalDiv = document.getElementById('team-rival');
    rivalDiv.innerHTML = '<h2>상대 전적</h2>';

    if (rivalData.error) {
        rivalDiv.innerHTML += `<p>${rivalData.error}</p>`;
        return;
    }

    rivalData.forEach(record => {
        rivalDiv.innerHTML += `
            <p>상대팀: ${record.rival}</p>
            <p>승: ${record.wins}, 무: ${record.draws}, 패: ${record.losses}, 승률: ${record.win_rate}</p>
        `;
    });
}

function displayTeamDetails(detailData) {
    const detailDiv = document.getElementById('team-details');
    detailDiv.innerHTML = '<h2>팀 상세 기록</h2>';

    if (detailData.error) {
        detailDiv.innerHTML += `<p>${detailData.error}</p>`;
        return;
    }

    detailData.forEach(detail => {
        detailDiv.innerHTML += `
            <p>${detail.year}년 ${detail.team}:</p>
            <ul>
                <li>WAR: ${detail.war}</li>
                <li>oWAR: ${detail.owar}</li>
                <li>dWAR: ${detail.dwar}</li>
                <li>경기 수: ${detail.games}</li>
                <li>타석 수: ${detail.plate_appearances}</li>
                <li>유효 타석 수: ${detail.effective_pa}</li>
                <li>타수: ${detail.at_bats}</li>
                <li>득점: ${detail.runs}</li>
                <li>안타: ${detail.hits}</li>
                <li>2루타: ${detail.two_b}</li>
                <li>3루타: ${detail.three_b}</li>
                <li>홈런: ${detail.home_runs}</li>
                <li>총 베이스: ${detail.total_bases}</li>
                <li>타점: ${detail.rbi}</li>
                <li>도루: ${detail.stolen_bases}</li>
                <li>도루 실패: ${detail.caught_stealing}</li>
                <li>볼넷: ${detail.walks}</li>
                <li>몸에 맞는 볼: ${detail.hit_by_pitch}</li>
                <li>고의 볼넷: ${detail.intentional_walks}</li>
                <li>삼진: ${detail.strikeouts}</li>
                <li>병살 타구: ${detail.grounded_into_double_play}</li>
                <li>희생타: ${detail.sacrifice_hits}</li>
                <li>희생플라이: ${detail.sacrifice_flies}</li>
                <li>타율: ${detail.batting_average}</li>
                <li>출루율: ${detail.on_base_percentage}</li>
                <li>장타율: ${detail.slugging_percentage}</li>
                <li>OPS: ${detail.on_base_plus_slugging}</li>
                <li>유효 타석당 득점: ${detail.runs_per_effective_pa}</li>
                <li>wRC+: ${detail.wrc_plus}</li>
            </ul>
        `;
    });
}