from django.urls import path
from .views import (
    CrawlAndSavePlayersView,
    PlayerRecordListView,
    CrawlGameDataView,
    GameRecordListView,
    TeamRankAPIView,
    TeamRankListView,
    PlayersCreateAPIView,
    PlayersListAPIView,
    SportsNewsAPIView,
    SportsNewsListAPIView,
    TeamRivalAPIView,
    TeamDetailAPIView,
    TeamDetailGetListView,
    TeamRivalGetAPIView,
    PlayerNumberAPIView,
)

urlpatterns = [
    # 크롤링 후 데이터를 저장하는 POST 요청용 URL
    path("news/crawl/", SportsNewsAPIView.as_view(), name="sports-news"),
    path(
        "players_rival/crawl/", CrawlAndSavePlayersView.as_view(), name="crawl-players"
    ),
    path("games/crawl/", CrawlGameDataView.as_view(), name="crawl-games"),
    path("teamrank/crawl/", TeamRankAPIView.as_view(), name="crawl-team-rank"),
    path("players/crawl/", PlayersCreateAPIView.as_view(), name="players-api"),
    path("teamrival/crawl/", TeamRivalAPIView.as_view(), name="players-api"),
    path("teamdetail/crawl/", TeamDetailAPIView.as_view(), name="players-api"),
    # 데이터 조회를 위한 GET 요청용 URL
    path(
        "players_rival/<str:player_number>/",
        PlayerRecordListView.as_view(),
        name="player-list",
    ),
    path("games/", GameRecordListView.as_view(), name="game-list"),
    path("teamrank/", TeamRankListView.as_view(), name="team-rank-list"),
    path("players/", PlayersListAPIView.as_view(), name="players-api"),
    path(
        "players/<str:player_number>/",
        PlayerNumberAPIView.as_view(),
        name="players-api",
    ),
    path("news/", SportsNewsListAPIView.as_view(), name="sports-news-list"),
    path("teamrival/", TeamRivalGetAPIView.as_view(), name="players-api"),
    path("teamdetail/", TeamDetailGetListView.as_view(), name="players-api"),
]
