import requests
import datetime
from .models import SportsNews  # SportsNews 모델 임포트
from homebase.config import API_KEY

# API_KEY를 상수로 설정
api_key = API_KEY


def news_crawling():
    url = "https://newsapi.org/v2/everything"  # Google News API URL
    params = {
        "q": "KBO OR 프로야구 OR 야구 OR 투수 OR 타자",  # 스포츠 관련 뉴스 검색
        "apiKey": api_key,  # API 키 사용
        "language": "ko",  # 한국어 뉴스
        "pageSize": 100,  # 가져올 뉴스 기사 수
        "sortBy": "publishedAt",  # 최신순으로 정렬
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

            # 중복 확인: URL을 기준으로 중복된 기사를 건너뜀
            news_item, created = SportsNews.objects.get_or_create(
                url=url,
                defaults={
                    "title": title,
                    "author": author,
                    "description": description,
                    "published_at": published_at,
                    "content": content,
                    "image_url": image_url,
                },
            )

            if created:  # 새롭게 생성된 경우에만 저장된 기사 수 증가
                total_saved += 1

        return total_saved  # 총 저장된 기사 수 반환

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP 에러 처리
        raise
    except Exception as err:
        print(f"Other error occurred: {err}")  # 다른 에러 처리
        raise
