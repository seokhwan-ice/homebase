from homebase.config import API_KEY
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from data.schedule import crawl_game_data
from data.players import crawl_players_data
from data.player_rival import crawl_playerrival_data
from data.team_rank import team_rank
from data.news import news_crawling
from .models import TeamRank, PlayerRecord, GameRecord, Players, SportsNews
from .serializers import (
    PlayerRecordSerializer,
    GameRecordSerializer,
    TeamRankSerializer,
    PlayersSerializer,
    SportsNewsListSerializer,
)


class CustomPagination(PageNumberPagination):
    page_size = 10  # 기본 페이지당 아이템 수
    page_size_query_param = "page_size"  # 쿼리 파라미터로 페이지당 아이템 수 조정 가능
    max_page_size = 100  # 최대 페이지당 아이템 수


# 내부적으로 일정 시간에 실행되게 하려면 핸들링 추가해야함@


# google News API 이용
class SportsNewsAPIView(APIView):
    def post(self, request):  # 실제 API 키로 변경

        try:
            total_saved = news_crawling()  # 크롤링 함수 호출

            return Response(
                {"message": f"{total_saved}개의 스포츠 뉴스 기사가 저장되었습니다."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
        total_records = crawl_playerrival_data()

        # 저장된 선수 기록 개수를 반환
        return Response(
            {"message": f"총 {total_records}개의 선수라이벌 기록이 저장되었습니다."}
        )


# 경기 기록 저장 뷰 (POST)
class CrawlGameDataView(APIView):
    def post(self, request):
        start_game_number = request.data.get("start_game_number", 20240001)  # 시작 번호
        end_game_number = request.data.get("end_game_number", 20242500)  # 끝 번호

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
        # 크롤링 작업을 실행하여 팀 데이터 가져오기
        total_records = team_rank()  # 크롤링 및 저장하는 함수 호출

        # 저장된 팀 기록 개수를 반환
        return Response(
            {"message": f"총 {total_records}개의 팀 기록이 저장되었습니다."},
            status=status.HTTP_201_CREATED,
        )


# 구글뉴스 조회 뷰(GET)
class SportsNewsListAPIView(APIView):
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        articles = SportsNews.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(
            articles, request
        )  # 페이지네이션 적용
        serializer = SportsNewsListSerializer(result_page, many=True)
        return paginator.get_paginated_response(
            serializer.data
        )  # 페이지네이션된 응답 반환


# 선수 기록 조회 뷰 (GET)
class PlayerRecordListView(APIView):
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        players = PlayerRecord.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(players, request)
        serializer = PlayerRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# 경기 기록 조회 뷰 (GET)
class GameRecordListView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        games = GameRecord.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(games, request)
        serializer = GameRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# 팀 순위 조회 뷰 (GET)
class TeamRankListView(APIView):
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        teams = TeamRank.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(teams, request)
        serializer = TeamRankSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# 전체 선수 정보 조회 뷰 (GET)
class PlayersListAPIView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        players = Players.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(players, request)
        serializer = PlayersSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)  # 성공 응답
