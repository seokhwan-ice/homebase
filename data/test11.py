import os
import django
from datetime import datetime

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homebase.settings")
django.setup()

import requests
from bs4 import BeautifulSoup
from data.models import Players  # 필요한 모델을 임포트하세요

# 크롤링할 URL
url = "https://statiz.sporki.com/player/?m=playerinfo&p_no=15435"

# 웹 페이지 요청
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 선수 정보 추출
profile = soup.find("div", class_="in_box")

# 선수 이미지
profile_img_tag = profile.find("div", class_="profile_img02")
profile_img = profile_img_tag.find("img")["src"] if profile_img_tag else None

# 선수 이름
name = profile.find("div", class_="name").text.strip()

# 선수 소속팀, 포지션, 타격 정보
con = profile.find("div", class_="con").find_all("span")
team = con[0].text.strip() if len(con) > 0 else ""
position = con[1].text.strip() if len(con) > 1 else ""
batter_hand = con[2].text.strip() if len(con) > 2 else ""

# 선수 상세 정보
man_info = profile.find("ul", class_="man_info").find_all("li")
birth_date_str = man_info[0].text.split(":")[1].strip() if len(man_info) > 0 else ""
birth_date = (
    datetime.strptime(birth_date_str, "%Y년 %m월 %d일").date()
    if birth_date_str
    else None
)
school = man_info[1].text.split(":")[1].strip() if len(man_info) > 1 else ""
draft_info = man_info[2].text.split(":")[1].strip() if len(man_info) > 2 else ""
active_years = man_info[3].text.split(":")[1].strip() if len(man_info) > 3 else ""
active_team = man_info[4].text.split(":")[1].strip() if len(man_info) > 4 else ""

# 데이터베이스에 저장
players = Players(
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
players.save()

# 결과 출력
print(
    f"선수 이름: {name}, 팀: {team}, 포지션: {position}, 생년월일: {birth_date}, 출신학교: {school}, 신인지명: {draft_info}, 활약연도: {active_years}, 활약팀: {active_team}"
)
