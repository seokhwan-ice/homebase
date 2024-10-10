// API 엔드포인트
const apiUrl = '/api/data/news/';  // Django의 API URL

// 페이지가 로드되면 API 요청
window.onload = function() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const newsList = document.getElementById('news-list');

            if (data.articles && data.articles.length > 0) {
                // 뉴스 데이터가 있을 경우
                data.articles.forEach(article => {
                    // 기사 리스트 아이템 생성
                    const listItem = document.createElement('li');

                    // 기사 제목 추가
                    const title = document.createElement('h2');
                    const link = document.createElement('a');
                    link.href = article.url;
                    link.target = '_blank';  // 새 창에서 열기
                    link.textContent = article.title;
                    title.appendChild(link);

                    // 기사 설명 추가
                    const description = document.createElement('p');
                    description.textContent = article.description;

                    // 기사 출처와 날짜 추가
                    const source = document.createElement('p');
                    source.innerHTML = `<strong>출처:</strong> ${article.source.name} | <strong>작성일:</strong> ${new Date(article.publishedAt).toLocaleDateString()}`;

                    // 리스트 아이템에 추가
                    listItem.appendChild(title);
                    listItem.appendChild(description);
                    listItem.appendChild(source);

                    // 뉴스 리스트에 추가
                    newsList.appendChild(listItem);
                });
            } else {
                // 뉴스가 없을 경우
                newsList.innerHTML = '<p>현재 KBO 관련 뉴스가 없습니다.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching news:', error);
            const newsList = document.getElementById('news-list');
            newsList.innerHTML = '<p>뉴스를 가져오는 중 오류가 발생했습니다.</p>';
        });
};