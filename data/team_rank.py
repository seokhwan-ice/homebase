import os
import django
import requests
from bs4 import BeautifulSoup
from data.models import TeamRank  # 모델 임포트

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homebase.settings")
django.setup()

# 크롤링할 URL
base_url = "https://statiz.sporki.com/season/"
url = f"{base_url}?m=teamoverall&year=2024"

# 웹 페이지 요청
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 팀 랭킹 데이터 추출
teams = []

# 팀 랭킹 데이터가 포함된 table의 tbody 선택
performance_table = soup.select(".box_cont .table_type03 tbody tr")

# 각 팀 데이터 추출 및 저장
for row in performance_table:
    cells = row.find_all("td")

    # 데이터가 충분히 있는지 확인
    if len(cells) >= 8:
        try:
            rank = int(cells[0].text.strip())  # 순위
            team_info = cells[1].find("a")
            team_name = team_info.text.strip()  # 팀 이름
            logo_url = team_info.find("img")["src"]  # 로고 URL
            games = int(cells[2].text.strip())  # 경기 수
            wins = int(cells[3].text.strip())  # 승 수
            draws = int(cells[4].text.strip())  # 무승부 수
            losses = int(cells[5].text.strip())  # 패 수
            game_diff = float(cells[6].text.strip())  # 승차
            win_rate = float(cells[7].text.strip())  # 승률

            # 팀 데이터를 데이터베이스에 저장
            team_rank = TeamRank(
                rank=rank,
                team_name=team_name,
                games_played=games,
                wins=wins,
                draws=draws,
                losses=losses,
                games_behind=game_diff,
                win_rate=win_rate,
                streak="",  # 이 필드는 크롤링하는 데이터에 맞게 수정하세요
                last_10_games="",  # 이 필드는 크롤링하는 데이터에 맞게 수정하세요
            )
            team_rank.save()  # 데이터베이스에 저장

            # 추후 활용을 위해 리스트에도 추가
            teams.append(
                {
                    "rank": rank,
                    "name": team_name,
                    "logo_url": logo_url,
                    "games": games,
                    "wins": wins,
                    "draws": draws,
                    "losses": losses,
                    "game_diff": game_diff,
                    "win_rate": win_rate,
                }
            )

        except ValueError as e:
            print(f"Error converting data: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# 결과 출력
print("팀 랭킹:")
for team in teams:
    print(
        f"순위: {team['rank']}, 팀명: {team['name']}, 로고: {team['logo_url']}, 경기 수: {team['games']}, 승: {team['wins']}, 무: {team['draws']}, 패: {team['losses']}, 승차: {team['game_diff']}, 승률: {team['win_rate']}"
    )
