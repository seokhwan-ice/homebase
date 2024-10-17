from celery import shared_task
from .news import news_crawling
from .player_rival import crawl_playerrival_data
from .players import crawl_players_data
from .schedule import crawl_game_data
from .team import fetch_team_data
from .teamdetail import fetch_teamdetail_data
from .team_rank import team_rank


@shared_task
def crawl_news():
    return news_crawling()  # 3시간마다 실행


@shared_task
def crawl_playerrival_data():
    return crawl_playerrival_data()  # 매일 01:00AM 실행


@shared_task
def crawl_players_data():
    return crawl_players_data()  # 매일 01:00AM 실행


@shared_task
def crawl_game_data():
    return crawl_game_data()  # 매일 01:00AM 실행


@shared_task
def fetch_team_data():
    return fetch_team_data()  # 매일 01:00AM 실행


@shared_task
def fetch_teamdetail_data():
    return fetch_teamdetail_data()  # 매일 01:00AM 실행


@shared_task
def team_rank():
    return team_rank()  # 매일 01:00AM 실행


# 실행 함수 셀러리 워커  celery -A homebase worker --loglevel=info
# 실행 함수 셀러리 비트  celery -A homebase beat --loglevel=info
