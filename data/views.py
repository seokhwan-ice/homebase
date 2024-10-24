import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from data.schedule import crawl_game_data
from data.players import crawl_players_data
from data.player_rival import crawl_playerrival_data
from data.team_rank import team_rank
from data.news import news_crawling
from data.team import fetch_team_data
from data.teamdetail import fetch_teamdetail_data
from data.youtube import crawl_youtube_videos
from .models import (
    TeamRank,
    PlayerRecord,
    GameRecord,
    Players,
    SportsNews,
    TeamRecord,
    TeamDetail,
    Video,
)
from data.data_weather import data_weatherforecast
from .serializers import (
    PlayerRecordSerializer,
    GameRecordSerializer,
    TeamRankSerializer,
    PlayersSerializer,
    SportsNewsListSerializer,
    TeamRecordSerializer,
    TeamDetailSerializer,
    TeamRankGetSerializer,
    TeamRecordGetSerializer,
    TeamDetailGetSerializer,
    VideoSerializer,
)

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 1000  # 기본 페이지당 아이템 수
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
class TeamRankAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # 크롤링 작업을 실행하여 팀 데이터 가져오기
        total_records = team_rank()  # 크롤링 및 저장하는 함수 호출

        # 저장된 팀 기록 개수를 반환
        return Response(
            {"message": f"총 {total_records}개의 팀 기록이 저장되었습니다."},
            status=status.HTTP_201_CREATED,
        )


# 팀 상대전적 저장 뷰 (POST)
class TeamRivalAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # 크롤링 작업을 실행하여 팀 데이터 가져오기
            total_records = fetch_team_data()  # 크롤링 및 저장하는 함수 호출

            return Response(
                {"message": f"총 {total_records}개의 팀 기록이 저장되었습니다."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# 팀 상세정보 크롤링 뷰(POST)
class TeamDetailAPIView(APIView):

    def post(self, request):
        """팀 통계 데이터를 크롤링하여 저장"""
        try:
            total_records = fetch_teamdetail_data()  # 크롤링하여 팀 데이터 저장

            return Response(
                {"message": f"총 {total_records}개의 팀 기록이 저장되었습니다."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# 유튜브 크롤링 뷰(POST)
class YouTubeVideoCrawlView(APIView):
    def post(self, request):
        query = request.data.get("query", None)  # 요청에서 검색어(query)를 가져옴
        if not query:
            return Response(
                {"error": "검색어(query)가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 크롤링 작업을 실행하여 데이터를 데이터베이스에 저장
            total_records = crawl_youtube_videos(query)  # 크롤링 함수 호출

            # 정상적으로 응답을 반환
            return Response(
                {"message": f"총 {total_records}개의 영상이 저장되었습니다."},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(f"크롤링 중 오류 발생: {str(e)}")  # 오류 로그
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
    def get(self, request, player_number):
        # player_number에 해당하는 모든 선수 데이터 가져오기
        player_records = PlayerRecord.objects.filter(player_number=player_number)

        # 플레이어가 없으면 404 반환
        if not player_records.exists():
            return Response({"error": "Player not found"}, status=404)

        # 직렬화하여 데이터 반환
        serializer = PlayerRecordSerializer(
            player_records, many=True
        )  # many=True로 설정
        return Response(serializer.data)


# 경기 기록 조회 뷰 (GET)
class GameRecordListView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        games = GameRecord.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(games, request)
        serializer = GameRecordSerializer(result_page, many=True)
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


# google News API 이용
class WeatherDataAPIView(APIView):
    def post(self, request):  # 실제 API 키로 변경

        try:
            total_record = data_weatherforecast()  # 크롤링 함수 호출

            return Response(
                {"message": f"{total_record} 기상 데이터가 저장되었습니다."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 특정 선수 정보 조회 뷰 (GET)
class PlayerNumberAPIView(APIView):

    def get(self, request, player_number):
        try:
            player = Players.objects.get(player_number=player_number)
            serializer = PlayersSerializer(player)
            return Response(serializer.data, status=status.HTTP_200_OK)  # 성공 응답
        except Players.DoesNotExist:
            return Response(
                {"error": "선수를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )  # 실패 응답


# 팀 순위 조회 뷰 (GET)
class TeamRankListView(APIView):
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        teams = TeamRank.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(teams, request)
        serializer = TeamRankSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# 팀 상대전적 조회 뷰 (GET)
class TeamRivalGetAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # 모든 팀 상대전적 데이터 조회
            rival_records = TeamRecord.objects.all()  # 모든 팀 상대전적 데이터 가져오기

            # 결과를 직렬화하여 반환할 데이터 형식 정의
            serializer = TeamRecordSerializer(rival_records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# 팀 상세기록 조회 뷰(GET)
class TeamDetailGetListView(APIView):
    def get(self, request):
        """팀 통계 데이터 목록 반환"""
        team_details = TeamDetail.objects.all()
        serializer = TeamDetailSerializer(team_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamRankDetailGetView(APIView):
    def get(self, request, team_number, *args, **kwargs):
        """특정 팀의 순위 정보 반환"""
        try:
            team_rank = TeamRank.objects.get(
                team_number=team_number
            )  # get()으로 단일 객체 가져오기
            serializer = TeamRankGetSerializer(team_rank)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TeamRank.DoesNotExist:
            return Response(
                {"error": "팀을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 팀 상대전적 조회 뷰 (GET)
class TeamRivalDetailGetAPIView(APIView):
    def get(self, request, team_number, *args, **kwargs):
        """특정 팀의 상대전적 정보 반환"""
        try:
            rival_records = TeamRecord.objects.filter(
                team_number=team_number
            )  # team_number로 필터링
            if not rival_records.exists():
                return Response(
                    {"error": "상대 전적을 찾을 수 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = TeamRecordGetSerializer(rival_records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 팀 상세기록 조회 뷰 (GET)
class TeamDetailDetailGetView(APIView):
    def get(self, request, team_number, *args, **kwargs):
        """특정 팀의 상세 통계 데이터 반환"""
        try:
            team_details = TeamDetail.objects.filter(
                team_number=team_number
            )  # team_number로 필터링
            if not team_details.exists():
                return Response(
                    {"error": "팀 상세 정보를 찾을 수 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = TeamDetailGetSerializer(team_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 유튜브 영상 조회 뷰(GET)
class YouTubeVideoGetListView(APIView):
    def get(self, request):
        videos = Video.objects.all()  # 모든 비디오 객체를 가져옴
        serializer = VideoSerializer(
            videos, many=True
        )  # 시리얼라이저를 사용하여 직렬화
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )  # 직렬화된 데이터와 함께 응답
