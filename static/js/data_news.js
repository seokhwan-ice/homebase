document.addEventListener('DOMContentLoaded', function () {
    // API에서 데이터를 가져와서 표시하는 함수
    axios.get('data/news/')  // API URL을 정확하게 설정
        .then(response => {
            console.log('받은 데이터:', response.data);  // 받아온 데이터 로그
            displayNews(response.data.articles);  // 'articles' 배열을 넘김
        })
        .catch(error => {
            console.error('뉴스 데이터를 가져오는 데 실패했습니다.', error);
            const newsList = document.getElementById("newsList");
            newsList.innerHTML = '<li>뉴스 데이터를 가져오는 데 실패했습니다. 나중에 다시 시도해주세요.</li>';
        });
}); // 이 괄호는 DOMContentLoaded 이벤트 핸들러의 끝입니다.

function displayNews(articles) {
    const newsList = document.getElementById("newsList");
    newsList.innerHTML = '';  // 기존 내용을 비움

    articles.forEach(function (article) {
        const newsItem = document.createElement('li');
        newsItem.classList.add('news-item');

        // 뉴스 제목과 링크
        const newsTitle = document.createElement('h2');
        const newsLink = document.createElement('a');
        newsLink.href = article.url;  // 기사 본문으로 링크
        newsLink.target = "_blank";  // 새 탭에서 열기
        newsLink.textContent = article.title;  // 제목 설정
        newsTitle.appendChild(newsLink);
        newsItem.appendChild(newsTitle); // 제목 추가

        // 뉴스 이미지 (이미지가 있을 경우에만 표시)
        if (article.image_url) {
            const newsImage = document.createElement('img');
            newsImage.src = article.image_url;
            newsImage.alt = article.title;
            newsImage.style.width = '300px';  // 이미지 너비 조정
            newsImage.style.height = 'auto';  // 비율에 맞춰 높이 자동 조정
            newsImage.style.objectFit = 'cover';
            newsItem.appendChild(newsImage);
        }

        // 뉴스 설명
        const newsDescription = document.createElement('p');
        newsDescription.textContent = article.description || '설명이 없습니다.';
        newsItem.appendChild(newsDescription);

        // 뉴스 출처
        const newsSource = document.createElement('p');
        newsSource.classList.add('source');
        newsSource.textContent = `기자: ${article.author || '알 수 없음'}`;
        newsItem.appendChild(newsSource);

        // 뉴스 발행일
        const newsDate = document.createElement('p');
        newsDate.classList.add('date');
        newsDate.textContent = `발행일: ${new Date(article.published_at).toLocaleDateString()}`;
        newsItem.appendChild(newsDate);

        newsList.appendChild(newsItem);
    });
}