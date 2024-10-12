document.addEventListener('DOMContentLoaded', function () {
    // API에서 데이터를 가져와서 표시하는 함수
    fetch('/news/')
        .then(response => response.json())
        .then(data => {
            displayNews(data.articles);
        })
        .catch(error => {
            console.error('뉴스 데이터를 가져오는 데 실패했습니다.', error);
            document.getElementById('newsList').innerHTML = `
                <li>뉴스 데이터를 가져오는 데 실패했습니다. 나중에 다시 시도해주세요.</li>`;
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
        if (article.image_url) {
            const newsImage = document.createElement('img');
            newsImage.src = article.image_url;
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

        // 뉴스 출처 (저자)
        const newsAuthor = document.createElement('p');
        newsAuthor.textContent = `기자: ${article.author || '출처 정보 없음'}`;
        newsItem.appendChild(newsAuthor);

        // 뉴스 발행일
        const newsDate = document.createElement('p');
        newsDate.textContent = `발행일: ${new Date(article.published_at).toLocaleDateString()}`;
        newsItem.appendChild(newsDate);

        newsList.appendChild(newsItem);
    });
}