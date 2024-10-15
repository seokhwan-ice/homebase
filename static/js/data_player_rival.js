async function fetchPlayerRivalData() {
    const urlParams = new URLSearchParams(window.location.search); // URL에서 쿼리 파라미터 가져오기
    const player_Number = urlParams.get('player_number'); // player_number 가져오기

    console.log('선수 번호:', player_Number); // 선수 번호 확인

    // player_number가 null인 경우 예외 처리
    if (!player_Number) {
        console.error('선수 번호가 없습니다.'); // 오류 메시지 로그
        return; // 함수 종료
    }

    try {
        const response = await axios.get(`data/players_rival/${player_Number}/`); // 선수 라이벌 기록 API 호출
        const playerRecords = response.data; // 응답 데이터

        console.log('응답 데이터:', playerRecords); // 응답 데이터 확인

        // 테이블에 선수 기록 추가
        const tableBody = document.querySelector("#player-records-table tbody");
        tableBody.innerHTML = ''; // 기존 내용 지우기

        // playerRecords가 배열인지 확인
        if (Array.isArray(playerRecords)) {
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
                    cell.textContent = record[field] !== undefined ? record[field] : '-'; // 값이 없을 경우 '-'
                    row.appendChild(cell);
                });

                tableBody.appendChild(row);
            });
        } else {
            console.error('playerRecords는 배열이 아닙니다.', playerRecords);
        }

    } catch (error) {
        console.error('선수 라이벌 기록을 가져오는 중 오류 발생:', error.response ? error.response.data : error.message);
    }
}
fetchPlayerRivalData();
// 페이지가 로드될 때 선수 라이벌 데이터 가져오기
window.onload = () => {
    console.log('현재 URL:', window.location.href); // 현재 URL 로그

};