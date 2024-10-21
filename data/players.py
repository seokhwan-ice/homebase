import os
import django
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from data.models import Players  # 필요한 모델을 임포트하세요

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homebase.settings")
django.setup()


def crawl_players_data(year=2024):

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
        f"{base_url}/team/?m=seasonBacknumber&t_code=5002&year=2024",  # LG트윈스
    ]
    total_records = 0  # 저장된 기록 수 초기화

    # 각 팀 URL을 순회하며 선수 정보 크롤링
    for team_url in team_urls:
        response = requests.get(team_url)
        soup = BeautifulSoup(response.text, "html.parser")
        uniform_divs = soup.find_all("div", class_="uniform")

        for div in uniform_divs:
            a_tags = div.find_all("a")
            for a in a_tags:
                player_url = f"{base_url}{a['href']}"
                # 선수 번호 추출 (p_no 값 추출)
                player_number = a["href"].split("p_no=")[-1]
                player_response = requests.get(player_url)
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

                team_name = con[0].text.strip() if len(con) > 0 else "정보 없음"
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
                    or team_name == "정보 없음"
                    or position == "정보 없음"
                ):
                    print(
                        f"선수 정보가 누락되었습니다: {name}, 팀: {team_name}, 포지션: {position}"
                    )
                    continue

                # 데이터베이스에 저장
                player = Players(
                    year=year,
                    player_number=player_number,
                    name=name,
                    team_name=team_name,
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

                # 결과 출력
                print(
                    f"선수 이름: {name}, 팀: {team_name}, 포지션: {position}, 생년월일: {birth_date}, 출신학교: {school}, "
                    f"신인지명: {draft_info}, 활약연도: {active_years}, 활약팀: {active_team}, 이미지 URL: {profile_img}"
                )

    return total_records  # 저장된 선수 기록의 개수 반환


# 중복된 크롤링에 대해서 덮어쓰기 하지 않는 부분 수정해야함@@@@
# 이미지 저장 하는걸 어떻게해야...?

# 팀안에 선수별로 정리하려면??
## 자바스크립트로 for문 돌면서 tag생성하면 됨.
## or if문으로 작성하는 방법도 있음.
