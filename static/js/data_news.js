const itemsPerPage = 9; // 한 페이지당 아이템 수
let currentPage = 1; // 현재 페이지
let newsArticles = []; // 전체 뉴스 기사 저장

document.addEventListener('DOMContentLoaded', function () {
    // API에서 데이터를 가져와서 표시하는 함수
    axios.get('data/news/')
        .then(response => {
            console.log('받은 데이터:', response.data); // 받아온 데이터 로그
            if (response.data && Array.isArray(response.data.results)) {
                newsArticles = response.data.results; // 전체 기사 저장
                displayNews(currentPage); // 첫 페이지 기사 표시
                setupPagination(); // 페이지네이션 설정
            } else {
                console.error('데이터 형식이 올바르지 않음:', response.data);
                const newsList = document.getElementById("newsList");
                newsList.innerHTML = '<li>유효한 뉴스 데이터를 찾을 수 없습니다.</li>';
            }
        })
        .catch(error => {
            console.error('뉴스 데이터를 가져오는 데 실패했습니다.', error);
            const newsList = document.getElementById("newsList");
            newsList.innerHTML = '<li>뉴스 데이터를 가져오는 데 실패했습니다. 나중에 다시 시도해주세요.</li>';
        });
});

function displayNews(page) {
    const newsList = document.getElementById("newsList");
    newsList.innerHTML = ''; // 기존 내용을 비움

    // 시작 인덱스와 종료 인덱스 계산
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;

    const articlesToDisplay = newsArticles.slice(start, end); // 현재 페이지에 해당하는 기사만 추출

    articlesToDisplay.forEach(function (article) {
        const newsItem = document.createElement('li');
        newsItem.classList.add('news-item');

        // 제목과 링크를 위한 컨테이너
        const titleContainer = document.createElement('div');
        titleContainer.classList.add('title-container');

        // 뉴스 제목과 링크
        const newsLink = document.createElement('a');
        newsLink.href = article.url; // 기사 본문으로 링크
        newsLink.target = "_blank"; // 새 탭에서 열기
        newsLink.textContent = article.title; // 제목 설정
        newsLink.style.textDecoration = 'none'; // 밑줄 제거
        titleContainer.appendChild(newsLink);
        newsItem.appendChild(titleContainer); // 제목 추가

        // 뉴스 이미지 (이미지가 있을 경우에만 표시)
        if (article.image_url) {
            const newsImage = document.createElement('img');
            newsImage.src = article.image_url;
            newsImage.alt = article.title;
            newsImage.style.width = '100%'; // 이미지 너비 조정
            newsImage.style.height = 'auto'; // 비율에 맞춰 높이 자동 조정
            newsImage.style.cursor = 'pointer'; // 클릭 가능 표시
            newsImage.addEventListener('click', function () {
                window.open(article.url, '_blank'); // 이미지 클릭 시 기사로 이동
            });
            newsItem.appendChild(newsImage); // 이미지 추가
        }

        newsList.appendChild(newsItem);
    });
}

function setupPagination() {
    const paginationContainer = document.getElementById('pagination-container');
    paginationContainer.innerHTML = ''; // 기존 내용 비움

    const totalPages = Math.ceil(newsArticles.length / itemsPerPage); // 총 페이지 수 계산

    for (let i = 1; i <= totalPages; i++) {
        const pageLink = document.createElement('a');
        pageLink.href = '#';
        pageLink.textContent = i; // 페이지 번호
        pageLink.addEventListener('click', function (event) {
            event.preventDefault(); // 기본 링크 동작 방지
            currentPage = i; // 현재 페이지 업데이트
            displayNews(currentPage); // 해당 페이지 뉴스 표시
            setupPagination(); // 페이지네이션 업데이트
        });

        // 현재 페이지에 active 클래스 추가
        if (i === currentPage) {
            pageLink.classList.add('active'); // 활성 페이지에 클래스 추가
        }

        paginationContainer.appendChild(pageLink); // 페이지 링크 추가
    }
}
