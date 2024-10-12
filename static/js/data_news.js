document.addEventListener('DOMContentLoaded', function () {
    // API에서 데이터를 가져와서 표시하는 함수
    fetch('/news/')
        .then(response => {
            console.log('응답 상태:', response.status);  // 응답 상태 코드 로그
            return response.json();
        })
        .then(data => {
            console.log('받은 데이터:', data);  // 받아온 데이터 로그
            displayNews(data.articles);
        })
        .catch(error => {
            console.error('뉴스 데이터를 가져오는 데 실패했습니다.', error);
        });
});

function displayNews(articles) {
    const newsList = document.getElementById("newsList");
    newsList.innerHTML = '';  // 기존 내용을 비움

    articles.forEach(function (article) {
        const newsItem = document.createElement('li');
        newsItem.classList.add('news-item');

        // 뉴스 제목과 링크
        const newsTitle = document.createElement('h2');
        const newsLink = document.createElement('a');
        newsLink.href = article.url;
        newsLink.target = "_blank";
        newsLink.textContent = article.title;
        newsTitle.appendChild(newsLink);

        // 뉴스 이미지 (이미지가 있을 경우에만 표시)
        if (article.urlToImage) {
            const newsImage = document.createElement('img');
            newsImage.src = article.urlToImage;
            newsImage.alt = article.title;
            newsImage.style.width = '100%';
            newsImage.style.maxHeight = '200px';
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
        newsSource.textContent = `출처: ${article.source.name || '출처 정보 없음'}`;
        newsItem.appendChild(newsSource);

        // 뉴스 발행일
        const newsDate = document.createElement('p');
        newsDate.classList.add('date');
        newsDate.textContent = `발행일: ${new Date(article.publishedAt).toLocaleDateString()}`;
        newsItem.appendChild(newsDate);

        newsList.appendChild(newsItem);
    });
}