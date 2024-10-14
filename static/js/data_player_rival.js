let currentPage = 1;  // 현재 페이지
        let totalPages = 0;   // 총 페이지 수

        function fetchPlayerRecords(page = 1) {
            axios.get(`data/players_rival/?page=${page}`) // API URL 확인
                .then(response => {
                    const playerRecords = response.data.results;  // 페이지네이션 결과
                    totalPages = response.data.total_pages; // 총 페이지 수
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

                    updatePaginationButtons();
                })
                .catch(error => {
                    console.error("데이터를 가져오는 중 오류 발생:", error);
                });
        }

        function changePage(direction) {
            currentPage += direction;
            fetchPlayerRecords(currentPage);
        }

        function updatePaginationButtons() {
            const prevButton = document.getElementById("prev-page");
            const nextButton = document.getElementById("next-page");

            prevButton.disabled = currentPage === 1;
            nextButton.disabled = currentPage === totalPages;
        }

        // 페이지가 로드될 때 데이터 가져오기
        document.addEventListener("DOMContentLoaded", () => {
            fetchPlayerRecords(currentPage);
        });