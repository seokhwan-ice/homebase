from django.urls import path
from .views import (
    CrawlAndSavePlayersView,
    PlayerRecordListView,
    CrawlGameDataView,
    GameRecordListView,
    TeamRecordAPIView,
    TeamRankListView,
    PlayersCreateAPIView,
)

urlpatterns = [
    # 크롤링 후 데이터를 저장하는 POST 요청용 URL
    path(
        "players_rival/crawl/", CrawlAndSavePlayersView.as_view(), name="crawl-players"
    ),
    path("games/crawl/", CrawlGameDataView.as_view(), name="crawl-games"),
    path("teamrank/crawl/", TeamRecordAPIView.as_view(), name="crawl-team-rank"),
    # 데이터 조회를 위한 GET 요청용 URL
    path("players_rival/", PlayerRecordListView.as_view(), name="player-list"),
    path("games/", GameRecordListView.as_view(), name="game-list"),
    path("teamrank/", TeamRankListView.as_view(), name="team-rank-list"),
    path("players/", PlayersCreateAPIView.as_view(), name="players-api"),
]
