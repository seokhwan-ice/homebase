import requests
from .models import SportsNews  # SportsNews 모델 임포트
from homebase.config import API_KEY

# API_KEY를 상수로 설정
api_key = API_KEY


def news_crawling():
    url = "https://newsapi.org/v2/everything"  # Google News API URL
    params = {
        "q": "KBO",  # 스포츠 관련 뉴스 검색
        "apiKey": api_key,  # API 키 사용
        "language": "ko",  # 한국어 뉴스
        "pageSize": 30,  # 가져올 뉴스 기사 수
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTPError 발생 시 예외 처리

        headlines_data = response.json()
        articles = headlines_data.get("articles", [])
        total_saved = 0  # 저장된 기사 수

        for article in articles:
            # 필요한 데이터 추출
            title = article.get("title")
            author = article.get("author")  # 기자 이름
            description = article.get("description")
            url = article.get("url")
            published_at = article.get("publishedAt")
            content = article.get("content")  # 기사 내용
            image_url = article.get("urlToImage")

            # SportsNews 모델 인스턴스 생성
            news_item = SportsNews(
                title=title,
                author=author,  # 기자 이름 저장
                description=description,
                url=url,
                published_at=published_at,
                content=content,  # 기사 내용 저장
                image_url=image_url,
            )
            # 데이터베이스에 저장
            news_item.save()
            total_saved += 1  # 저장된 기사 수 증가

        return total_saved  # 총 저장된 기사 수 반환

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP 에러 처리
        raise
    except Exception as err:
        print(f"Other error occurred: {err}")  # 다른 에러 처리
        raise
