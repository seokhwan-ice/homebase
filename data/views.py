import requests
from homebase.config import API_KEY
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from data.schedule import crawl_game_data
from data.players import crawl_players_data
from data.player_rival import crawl_player_data
from .models import TeamRank, PlayerRecord, GameRecord, Players
from .serializers import (
    PlayerRecordSerializer,
    GameRecordSerializer,
    TeamRankSerializer,
    PlayersSerializer,
)

api_key = API_KEY


# 내부적으로 일정 시간에 실행되게 하려면 핸들링 추가해야함@


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


class PlayersCreateAPIView(APIView):
    def post(self, request):
        # 크롤링 작업을 실행하여 데이터를 데이터베이스에 저장
        total_records = crawl_players_data()  # 크롤링 함수 호출

        # 저장된 선수 기록 개수를 반환
        return Response(
            {"message": f"총 {total_records}개의 선수 기록이 저장되었습니다."}
        )


# 선수 기록 저장 뷰 (POST)
class CrawlAndSavePlayersView(APIView):
    def post(self, request, *args, **kwargs):
        # 크롤링 작업을 실행하여 데이터를 데이터베이스에 저장
        total_records = crawl_player_data()

        # 저장된 선수 기록 개수를 반환
        return Response(
            {"message": f"총 {total_records}개의 선수라이벌 기록이 저장되었습니다."}
        )


# 경기 기록 저장 뷰 (POST)
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


# 팀 순위 데이터 저장 뷰 (POST)
class TeamRecordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # 요청 데이터에서 팀 정보 추출
        teams_data = (
            request.data
        )  # 예: [{"rank": 1, "name": "팀명", "games_played": 10, "wins": 7, ...}, {...}]

        for team_data in teams_data:
            # 각 팀 데이터를 DB에 저장
            team_record = TeamRank(
                rank=team_data.get("rank"),
                name=team_data.get("name"),
                games_played=team_data.get("games_played"),
                wins=team_data.get("wins"),
                draws=team_data.get("draws"),
                losses=team_data.get("losses"),
                games_behind=team_data.get("games_behind"),
                win_percentage=team_data.get("win_percentage"),
                streak=team_data.get("streak"),
                recent_10_games=team_data.get("recent_10_games"),
            )
            team_record.save()  # 데이터베이스에 저장

        return Response(
            {"message": "팀 데이터가 성공적으로 저장되었습니다."},
            status=status.HTTP_201_CREATED,
        )


# 선수 기록 조회 뷰 (GET)
class PlayerRecordListView(APIView):
    def get(self, request, *args, **kwargs):
        players = PlayerRecord.objects.all()
        serializer = PlayerRecordSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 경기 기록 조회 뷰 (GET)
class GameRecordListView(APIView):
    def get(self, request):
        games = GameRecord.objects.all()
        serializer = GameRecordSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 팀 순위 조회 뷰 (GET)
class TeamRankListView(APIView):
    def get(self, request, *args, **kwargs):
        teams = TeamRank.objects.all()
        serializer = TeamRankSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 전체 선수 정보 조회 뷰 (GET)
class PlayersListAPIView(APIView):
    def get(self, request):
        players = Players.objects.all()  # 모든 선수 정보 조회
        serializer = PlayersSerializer(players, many=True)  # 직렬화
        return Response(serializer.data, status=status.HTTP_200_OK)  # 성공 응답
