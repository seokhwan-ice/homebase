import requests
from data.players import crawl_player_data
from config import API_KEY
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from data.schedule import crawl_game_data

# from .schedule import crawl_game_data

api_key = API_KEY


# google News API 이용
class SportsNewsAPIView(APIView):
    def get(self, request):
        url = "https://newsapi.org/v2/everything"  # Google News API URL
        params = {
            "q": "KBO",  # 스포츠 관련 뉴스 검색
            "apiKey": api_key,
            "language": "ko",  # 한국어 뉴스
            "pageSize": 100,  # 가져올 뉴스 기사 수 (필요에 따라 조정 가능)
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            headlines_data = response.json()
            return Response(headlines_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "뉴스를 가져오는 데 실패했습니다."},
                status=response.status_code,
            )


class CrawlAndSavePlayersView(APIView):
    def post(self, request, *args, **kwargs):
        # 크롤링 작업을 실행하여 데이터를 데이터베이스에 저장
        total_records = crawl_player_data()

        # 저장된 선수 기록 개수를 반환
        return Response(
            {"message": f"총 {total_records}개의 선수 기록이 저장되었습니다."}
        )


class CrawlGameDataView(APIView):
    def post(self, request):
        start_game_number = request.data.get("start_game_number", 20240001)  # 시작 번호
        end_game_number = request.data.get("end_game_number", 20250000)  # 끝 번호

        # 유효성 검사
        if start_game_number is None or end_game_number is None:
            return Response(
                {"error": "start_game_number and end_game_number are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_game_number = int(start_game_number)
            end_game_number = int(end_game_number)
        except ValueError:
            return Response(
                {"error": "start_game_number and end_game_number must be integers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 크롤링 수행
        total_records = crawl_game_data(start_game_number, end_game_number)

        return Response(
            {"message": f"Crawled {total_records} game records."},
            status=status.HTTP_201_CREATED,
        )
