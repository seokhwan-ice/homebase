import requests
from bs4 import BeautifulSoup

# 게임 번호
game_number = 20240001
base_url = "https://statiz.sporki.com/schedule/"
url = f"{base_url}?m=summary&s_no={game_number}"

# HTTP 요청 보내기
response = requests.get(url)

# 응답이 성공적인지 확인
if response.status_code == 200:
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")

    # 점수 리스트 초기화
    inning_scores_team_1 = []
    inning_scores_team_2 = []

    # 각 이닝의 점수를 가져오는 반복문 (예: 12이닝까지)
    for inning in range(12):
        # 팀 1의 점수 가져오기
        score_element_team_1 = soup.select_one(
            f"body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child(1) > td:nth-child({inning + 2}) > div"
        )

        # 팀 2의 점수 가져오기
        score_element_team_2 = soup.select_one(
            f"body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child(2) > td:nth-child({inning + 2}) > div"
        )

        # 팀 1 점수 처리
        if score_element_team_1 is not None:
            score_text_team_1 = score_element_team_1.contents[
                0
            ].strip()  # <p> 앞의 숫자 가져오기
            print(
                f"팀 1 이닝 {inning + 1} 점수 데이터: '{score_text_team_1}'"
            )  # 데이터 확인
            try:
                inning_scores_team_1.append(
                    int(score_text_team_1)
                )  # 정수로 변환하여 추가
            except ValueError:
                inning_scores_team_1.append(0)  # 숫자로 변환 실패 시 0 추가
        else:
            print(f"팀 1 이닝 {inning + 1} 점수 데이터가 없습니다.")
            inning_scores_team_1.append(0)

        # 팀 2 점수 처리
        if score_element_team_2 is not None:
            score_text_team_2 = score_element_team_2.contents[
                0
            ].strip()  # <p> 앞의 숫자 가져오기
            print(
                f"팀 2 이닝 {inning + 1} 점수 데이터: '{score_text_team_2}'"
            )  # 데이터 확인
            try:
                inning_scores_team_2.append(
                    int(score_text_team_2)
                )  # 정수로 변환하여 추가
            except ValueError:
                inning_scores_team_2.append(0)  # 숫자로 변환 실패 시 0 추가
        else:
            print(f"팀 2 이닝 {inning + 1} 점수 데이터가 없습니다.")
            inning_scores_team_2.append(0)

    # R, H, E, B 값 추출
    def extract_stat(row, column):
        element = soup.select_one(
            f"body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child({row}) > td:nth-child({column}) > div"
        )
        return int(element.text.strip()) if element else 0  # 정수로 변환

    r_1, h_1, e_1, b_1 = [extract_stat(1, i) for i in range(14, 18)]
    r_2, h_2, e_2, b_2 = [extract_stat(2, i) for i in range(14, 18)]

    # 각 팀의 데이터를 테이블 형식으로 출력
    inning_scores_str_team_1 = ",".join(map(str, inning_scores_team_1))
    inning_scores_str_team_2 = ",".join(map(str, inning_scores_team_2))

    # 최종 결과 출력
    print(f"팀 1 이닝 점수: {inning_scores_str_team_1}, {r_1}, {h_1}, {e_1}, {b_1}")
    print(f"팀 2 이닝 점수: {inning_scores_str_team_2}, {r_2}, {h_2}, {e_2}, {b_2}")

else:
    print(f"HTTP 요청 실패: {response.status_code}")


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
        try:
            response = requests.get(team_url)
            response.raise_for_status()  # HTTP 요청이 실패하면 예외 발생
        except requests.exceptions.RequestException as e:
            print(f"팀 URL 요청 실패: {team_url}, 오류: {e}")
            continue  # 요청 실패 시 다음 URL로 넘어감

        soup = BeautifulSoup(response.text, "html.parser")
        uniform_divs = soup.find_all("div", class_="uniform")

        for div in uniform_divs:
            a_tags = div.find_all("a")
            for a in a_tags:
                player_url = f"{base_url}{a['href']}"
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

                # 데이터베이스에 저장
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

                # 결과 출력
                print(
                    f"선수 이름: {name}, 팀: {team}, 포지션: {position}, 생년월일: {birth_date}, 출신학교: {school}, "
                    f"신인지명: {draft_info}, 활약연도: {active_years}, 활약팀: {active_team}, 이미지 URL: {profile_img}"
                )

    return total_records  # 저장된 선수 기록의 개수 반환


import os
import django
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from data.models import Players  # 필요한 모델을 임포트하세요

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homebase.settings")
django.setup()

# User-Agent를 정의합니다.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


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
            response = requests.get(team_url, headers=headers)
            if response.status_code != 200:
                print(
                    f"Failed to fetch {team_url}, Status Code: {response.status_code}"
                )
                continue
        except Exception as e:
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

                # 각 요청 사이에 2초 대기
                time.sleep(2)

                try:
                    # player_url에도 headers를 추가하여 요청
                    player_response = requests.get(player_url, headers=headers)
                    if player_response.status_code != 200:
                        print(f"Failed to fetch player data: {player_url}")
                        continue
                except Exception as e:
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

                # 데이터베이스에 저장
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
