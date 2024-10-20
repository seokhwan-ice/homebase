from googleapiclient.discovery import build
from .models import Video
from django.utils.dateparse import parse_datetime
from homebase import config  # config.py에서 API 키 가져오기


def crawl_youtube_videos(query):
    api_key = config.YOUTUBE_API_KEY
    youtube = build("youtube", "v3", developerKey=api_key)

    total_records = 0  # 저장된 비디오 개수 초기화
    next_page_token = None  # 다음 페이지 토큰 초기화

    while True:
        # 비디오 검색 요청
        request = youtube.search().list(
            part="id,snippet",
            q=query,
            type="video",
            maxResults=50,  # 최대 50개 결과
            order="viewCount",
            pageToken=next_page_token,  # 다음 페이지 토큰
        )

        response = request.execute()

        # 검색 결과를 데이터베이스에 저장
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            publish_time = parse_datetime(item["snippet"]["publishedAt"])
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # "응원가"가 제목이나 설명에 포함된 경우만 저장
            if "응원가" in title or "응원가" in description:
                Video.objects.get_or_create(
                    video_id=video_id,
                    defaults={
                        "title": title,
                        "description": description,
                        "publish_time": publish_time,
                        "video_url": video_url,
                    },
                )
                total_records += 1  # 저장된 비디오 개수 증가

        # 다음 페이지 토큰이 없으면 종료
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # 더 이상 페이지가 없으면 종료

    return total_records  # 총 저장된 개수 반환
