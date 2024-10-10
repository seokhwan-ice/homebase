import os
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homebase.settings")
django.setup()

# 모델 임포트
from data.models import Players


def crawl_players_data():
    base_url = "https://statiz.sporki.com"  # 기본 URL 설정
    team_urls = [
        f"{base_url}/team/?m=seasonBacknumber&t_code=2002&year=2024",  # 기아타이거즈
        f"{base_url}/team/?m=seasonBacknumber&t_code=6002&year=2024",  # 두산베어스
        f"{base_url}/team/?m=seasonBacknumber&t_code=3001&year=2024",  # 롯데자이언츠
        f"{base_url}/team/?m=seasonBacknumber&t_code=11001&year=2024",  # NC다이노스
        f"{base_url}/team/?m=seasonBacknumber&t_code=10001&year=2024",  # 키움히어로즈
        f"{base_url}/team/?m=seasonBacknumber&t_code=1001&year=2024",  # 삼성라이온즈
        f"{base_url}/team/?m=seasonBacknumber&t_code=7002&year=2024",  # 한화이글스
        f"{base_url}/team/?m=seasonBacknumber&t_code=12001&year=2024",  # KT위즈
        f"{base_url}/team/?m=seasonBacknumber&t_code=9002&year=2024",  # SSG랜더스
    ]
    total_records = 0  # 저장된 기록 수 초기화

    # 각 팀 URL을 순회하며 선수 정보 크롤링
    for team_url in team_urls:
        print(f"크롤링 시작: {team_url}")  # 각 팀 크롤링 시작 로그 추가

        try:
            # headers를 추가하여 요청
            response = requests.get(team_url, headers=headers, timeout=10)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        except requests.RequestException as e:
            print(f"Error fetching data from {team_url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        uniform_divs = soup.find_all("div", class_="uniform")

        if not uniform_divs:
            print(f"No player data found for {team_url}")
            continue

        for div in uniform_divs:
            a_tags = div.find_all("a")
            for a in a_tags:
                player_url = f"{base_url}{a['href']}"
                print(f"선수 크롤링 중: {player_url}")  # 각 선수 크롤링 시작 로그 추가

                # 각 요청 사이에 랜덤 대기
                time.sleep(random.uniform(1.5, 3.0))

                try:
                    # player_url에도 headers를 추가하여 요청
                    player_response = requests.get(
                        player_url, headers=headers, timeout=10
                    )
                    player_response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
                except requests.RequestException as e:
                    print(f"Error fetching player data from {player_url}: {e}")
                    continue

                player_soup = BeautifulSoup(player_response.text, "html.parser")
                profile = player_soup.find("div", class_="in_box")

                if not profile:
                    print(f"선수 프로필을 찾을 수 없습니다: {player_url}")
                    continue

                profile_img_tag = profile.find("div", class_="profile_img02")
                profile_img = (
                    profile_img_tag.find("img")["src"] if profile_img_tag else None
                )
                name = (
                    profile.find("div", class_="name").text.strip()
                    if profile.find("div", class_="name")
                    else "정보 없음"
                )
                con = profile.find("div", class_="con").find_all("span")

                team = con[0].text.strip() if len(con) > 0 else "정보 없음"
                position = con[1].text.strip() if len(con) > 1 else "정보 없음"
                batter_hand = con[2].text.strip() if len(con) > 2 else "정보 없음"

                man_info = profile.find("ul", class_="man_info").find_all("li")
                birth_date_str = (
                    man_info[0].text.split(":")[1].strip() if len(man_info) > 0 else ""
                )
                birth_date = (
                    datetime.strptime(birth_date_str, "%Y년 %m월 %d일").date()
                    if birth_date_str
                    else None
                )
                school = (
                    man_info[1].text.split(":")[1].strip()
                    if len(man_info) > 1
                    else "정보 없음"
                )
                draft_info = (
                    man_info[2].text.split(":")[1].strip()
                    if len(man_info) > 2
                    else "정보 없음"
                )
                active_years = (
                    man_info[3].text.split(":")[1].strip()
                    if len(man_info) > 3
                    else "정보 없음"
                )
                active_team = (
                    man_info[4].text.split(":")[1].strip()
                    if len(man_info) > 4
                    else "정보 없음"
                )

                # 필수 정보가 모두 있는지 확인
                if (
                    name == "정보 없음"
                    or team == "정보 없음"
                    or position == "정보 없음"
                ):
                    print(
                        f"선수 정보가 누락되었습니다: {name}, 팀: {team}, 포지션: {position}"
                    )
                    continue

                try:
                    player = Players(
                        name=name,
                        team=team,
                        position=position,
                        batter_hand=batter_hand,
                        birth_date=birth_date,
                        school=school,
                        draft_info=draft_info,
                        active_years=active_years,
                        active_team=active_team,
                        profile_img=profile_img,
                    )
                    player.save()
                    total_records += 1  # 저장된 기록 수 증가
                    print(f"Saved player: {name}, 팀: {team}, 포지션: {position}")
                except Exception as e:
                    print(f"Error saving player {name}: {e}")
                    continue
        print(f"총 {total_records}명의 선수가 저장되었습니다.")  # 최종 결과 출력
        return total_records  # 저장된 선수 기록의 개수 반환
