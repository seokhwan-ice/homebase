from django.urls import path
from .views import (
    SportsNewsAPIView,
    CrawlAndSavePlayersView,
    CrawlGameDataView,
    TeamRecordAPIView,
)

app_name = "data"
urlpatterns = [
    path("sports_news/", SportsNewsAPIView.as_view(), name="sports_news"),
    path("crawl_players/", CrawlAndSavePlayersView.as_view(), name="crawl_players"),
    path("schedule/", CrawlGameDataView.as_view(), name="schedule_api"),
    path("team_ranking/", TeamRecordAPIView.as_view(), name="crawl_team_ranking"),
]
