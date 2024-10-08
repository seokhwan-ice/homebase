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
