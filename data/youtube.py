from googleapiclient.discovery import build


def search_youtube_videos(api_key, query):
    youtube = build("youtube", "v3", developerKey=api_key)

    # 비디오 검색 요청
    request = youtube.search().list(
        part="id,snippet",
        q=query,
        type="video",  # 비디오만 검색
        maxResults=10,  # 최대 10개 결과
        order="date",  # 최신 순으로 정렬
    )

    response = request.execute()

    # 검색 결과 출력
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        publish_time = item["snippet"]["publishedAt"]

        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Published At: {publish_time}")
        print(f"Video URL: https://www.youtube.com/watch?v={video_id}\n")


# 사용 예
API_KEY = "AIzaSyAs7cCBA8xonFbtM1zbH-cbqTf8PeJjj64"  # 본인의 API 키
search_youtube_videos(API_KEY, "두산베어스+응원가")  # 원하는 키워드로 검색
### 아직 구현중###