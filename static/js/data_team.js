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

    const team = teams.find(t => t.logo === `${rankData.team_number}.png`);
    if (team) {
        teamLogo.src = `/static/images/${team.logo}`;
        teamName.innerText = team.name;
    } else {
        teamLogo.src = `/static/images/default_logo.png`;
        teamName.innerText = "알 수 없는 팀";
    }

    // 표로 출력
    rankDiv.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>순위</th>
                    <th>경기수</th>
                    <th>승</th>
                    <th>무</th>
                    <th>패</th>
                    <th>승률</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${rankData.rank}</td>
                    <td>${rankData.games_played}</td>
                    <td>${rankData.wins}</td>
                    <td>${rankData.draws}</td>
                    <td>${rankData.losses}</td>
                    <td>${rankData.win_rate}</td>
                </tr>
            </tbody>
        </table>
    `;
}

function displayRivalRecords(rivalData) {
    const rivalDiv = document.getElementById('team-rival');


    if (rivalData.error) {
        rivalDiv.innerHTML += `<p>${rivalData.error}</p>`;
        return;
    }

    let tableHTML = `
        <table>
            <tr>
                <th>상대팀</th>
                <th>승</th>
                <th>무</th>
                <th>패</th>
                <th>승률</th>
            </tr>
    `;

    rivalData.forEach(record => {
        tableHTML += `
            <tr>
                <td>${record.rival}</td>
                <td>${record.wins}</td>
                <td>${record.draws}</td>
                <td>${record.losses}</td>
                <td>${record.win_rate}</td>
            </tr>
        `;
    });

    tableHTML += `</table>`;
    rivalDiv.innerHTML += tableHTML;
}

function displayTeamDetails(detailData) {
    const detailDiv = document.getElementById('team-details');


    if (detailData.error) {
        detailDiv.innerHTML += `<p>${detailData.error}</p>`;
        return;
    }

    let tableHTML = `
        <table>
            <tr>
                <th>Year</th>
                <th>War</th>
                <th>oWAR</th>
                <th>dWAR</th>
                <th>G</th>
                <th>PA</th>
                <th>ePA</th>
                <th>AB</th>
                <th>R</th>
                <th>H</th>
                <th>2B</th>
                <th>3B</th>
                <th>HR</th>
                <th>TB</th>
                <th>RBI</th>
                <th>SB</th>
                <th>CS</th>
                <th>BB</th>
                <th>HP</th>
                <th>IB</th>
                <th>SO</th>
                <th>GDP</th>
                <th>SH</th>
                <th>SF</th>
                <th>AVG</th>
                <th>OBP</th>
                <th>SLG</th>
                <th>OPS</th>
                <th>R/ePA</th>
                <th>wRC+</th>
            </tr>
    `;

    detailData.forEach(detail => {
        tableHTML += `
            <tr>
                <td>${detail.year}</td>
                <td>${detail.war}</td>
                <td>${detail.owar}</td>
                <td>${detail.dwar}</td>
                <td>${detail.games}</td>
                <td>${detail.plate_appearances}</td>
                <td>${detail.effective_pa}</td>
                <td>${detail.at_bats}</td>
                <td>${detail.runs}</td>
                <td>${detail.hits}</td>
                <td>${detail.two_b}</td>
                <td>${detail.three_b}</td>
                <td>${detail.home_runs}</td>
                <td>${detail.total_bases}</td>
                <td>${detail.rbi}</td>
                <td>${detail.stolen_bases}</td>
                <td>${detail.caught_stealing}</td>
                <td>${detail.walks}</td>
                <td>${detail.hit_by_pitch}</td>
                <td>${detail.intentional_walks}</td>
                <td>${detail.strikeouts}</td>
                <td>${detail.grounded_into_double_play}</td>
                <td>${detail.sacrifice_hits}</td>
                <td>${detail.sacrifice_flies}</td>
                <td>${detail.batting_average}</td>
                <td>${detail.on_base_percentage}</td>
                <td>${detail.slugging_percentage}</td>
                <td>${detail.on_base_plus_slugging}</td>
                <td>${detail.runs_per_effective_pa}</td>
                <td>${detail.wrc_plus}</td>
            </tr>
        `;
    });

    tableHTML += `</table>`;
    detailDiv.innerHTML += tableHTML;
}