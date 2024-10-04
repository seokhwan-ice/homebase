# # # #### 절대 삭제 금지###
# # # ### 해야할거
# # # ### 데이터 베이스 저장하는법 데이터 형태 잘 생각해서 저장하기!!!
# # # ### 전체 페이지(2. 팀별 반복문 돌리기)
# # # ### 모델정의
# # # ### 유니폼 a태그 값에 href가 있음.
# import requests
# from bs4 import BeautifulSoup
#
# # 선수 목록을 가져오는 URL
# base_url = "https://statiz.sporki.com"
# url = f"{base_url}/team/?m=seasonBacknumber&t_code=2002&year=2024"
#
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
#
# # 클래스가 'uniform'인 모든 div 태그 선택
# uniform_divs = soup.find_all("div", class_="uniform")
#
# # 선수 데이터를 저장할 딕셔너리
# player_data = {}
#
# # 각 uniform div에서 a 태그의 href와 텍스트 저장
# for div in uniform_divs:
#     a_tags = div.find_all("a")
#     for a in a_tags:
#         # href에서 playerinfo 값을 rival로 변경
#         href_value = a["href"].replace("playerinfo", "rival")
#
#         # 상대 경로를 절대 경로로 변경
#         player_url = f"{base_url}{href_value}"
#
#         # 선수의 rival 페이지에서 테이블 내용 크롤링
#         player_response = requests.get(player_url)
#         player_soup = BeautifulSoup(player_response.text, "html.parser")
#
#         # 예를 들어, 'table'이라는 클래스를 가진 테이블을 찾는다고 가정
#         table = player_soup.find(
#             "table"
#         )  # 적절한 선택자를 사용하여 원하는 테이블을 선택하세요
#
#         # 테이블의 내용을 리스트로 저장
#         if table:
#             rows = table.find_all("tr")
#             table_data = []
#             for row in rows:
#                 cols = row.find_all("td")
#                 cols = [ele.text.strip() for ele in cols]
#                 if cols:  # 빈 리스트는 저장하지 않음
#                     table_data.append(cols)
#
#             # 딕셔너리에 저장
#             player_data[a.text] = table_data
#
# # 결과 출력
# print(player_data)

# import requests
# from bs4 import BeautifulSoup
#
#
# def safe_convert_to_int(value):
#     if value is not None and value.isdigit():
#         return int(value)
#     return 0  # 기본값으로 0을 반환
#
#
# game_number = 20240001
# base_url = "https://statiz.sporki.com/schedule/"
# url = f"{base_url}?m=summary&s_no={game_number}"
# response = requests.get(url)
#
# # HTTP 요청 보내기
# soup = BeautifulSoup(response.text, "html.parser")
#
# # 팀 점수를 저장할 리스트
# inning_scores_team_1 = [0] * 12
# inning_scores_team_2 = [0] * 12
#
# # 점수 가져오기
# for inning in range(12):  # 0부터 11까지 반복
#     # 팀 1 선택자
#     score_1_selector = f"body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child(1) > td:nth-child({inning + 2}) > div.score"
#
#     # 팀 2 선택자
#     score_2_selector = f"body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child(2) > td:nth-child({inning + 2}) > div.score"
#
#     # 요소 선택
#     score_1_element = soup.select_one(score_1_selector)
#     score_2_element = soup.select_one(score_2_selector)
#
#     # 출력값 체크
#     print(
#         f"1이닝 {inning + 1} - 팀 1 요소: {score_1_element}, 팀 2 요소: {score_2_element}"
#     )
#
#     # 점수 저장
#     inning_scores_team_1[inning] = safe_convert_to_int(
#         score_1_element.text.strip()
#         if score_1_element and score_1_element.text.strip().isdigit()
#         else "0"
#     )
#     inning_scores_team_2[inning] = safe_convert_to_int(
#         score_2_element.text.strip()
#         if score_2_element and score_2_element.text.strip().isdigit()
#         else "0"
#     )
#
# # 점수 출력
# print(f"팀 1 점수: {inning_scores_team_1}")
# print(f"팀 2 점수: {inning_scores_team_2}")
#
# test_selector = "body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child(1) > td:nth-child(2) > div.score"
# test_element = soup.select_one(test_selector)
# print(test_element)


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

        # 팀 1 점수 출력
        print(f"팀 1 이닝 {inning + 1} 점수: {inning_scores_team_1[-1]}")

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

        # 팀 2 점수 출력
        print(f"팀 2 이닝 {inning + 1} 점수: {inning_scores_team_2[-1]}")

    # 최종 점수 출력
    print("최종 팀 1 점수:", inning_scores_team_1)
    print("최종 팀 2 점수:", inning_scores_team_2)
else:
    print(f"HTTP 요청 실패: {response.status_code}")
