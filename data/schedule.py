import requests
from bs4 import BeautifulSoup
from .models import GameRecord  # GameRecord 모델 임포트
from datetime import datetime  # datetime 모듈 임포트


def crawl_game_data(start_game_number, end_game_number):
    total_records = 0  # 총 크롤링한 레코드 수 초기화

    for game_number in range(start_game_number, end_game_number + 1):
        base_url = "https://statiz.sporki.com/schedule/"
        url = f"{base_url}?m=summary&s_no={game_number}"

        # HTTP 요청 보내기
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # 이닝 점수 가져오기
            inning_scores_team_1 = []
            inning_scores_team_2 = []

            for inning in range(12):
                score_element_team_1 = soup.select_one(
                    f"body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child(1) > td:nth-child({inning + 2}) > div"
                )
                score_element_team_2 = soup.select_one(
                    f"body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child(2) > td:nth-child({inning + 2}) > div"
                )

                # 팀 1 점수 처리
                if score_element_team_1 is not None:
                    score_text_team_1 = (
                        score_element_team_1.contents[0]
                        .strip()
                        .replace("%", "")
                        .replace(" ", "")
                    )  # 불필요한 문자 제거

                    try:
                        inning_scores_team_1.append(
                            int(score_text_team_1)
                        )  # 정수로 변환하여 추가
                    except ValueError:
                        inning_scores_team_1.append(0)  # 숫자로 변환 실패 시 0 추가
                else:
                    inning_scores_team_1.append(0)

                # 팀 2 점수 처리
                if score_element_team_2 is not None:
                    score_text_team_2 = (
                        score_element_team_2.contents[0]
                        .strip()
                        .replace("%", "")
                        .replace(" ", "")
                    )  # 불필요한 문자 제거
                    try:
                        inning_scores_team_2.append(
                            int(score_text_team_2)
                        )  # 정수로 변환하여 추가
                    except ValueError:
                        inning_scores_team_2.append(0)  # 숫자로 변환 실패 시 0 추가
                else:
                    inning_scores_team_2.append(0)

            # R, H, E, B 값 추출
            def extract_stat(row, column):
                element = soup.select_one(
                    f"body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child({row}) > td:nth-child({column}) > div"
                )
                if element is not None:
                    return int(element.text.strip())
                return 0

            # R, H, E, B 값 추출
            r_1, h_1, e_1, b_1 = [extract_stat(1, i) for i in range(14, 18)]
            r_2, h_2, e_2, b_2 = [extract_stat(2, i) for i in range(14, 18)]

            # 팀 1과 팀 2의 R, H, E, B 값을 JSON으로 저장
            r_h_e_b_team_1 = {"R": r_1, "H": h_1, "E": e_1, "B": b_1}
            r_h_e_b_team_2 = {"R": r_2, "H": h_2, "E": e_2, "B": b_2}

            # 날짜 처리
            date_text_element = soup.select_one(
                "body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_head"
            )

            if date_text_element is not None:
                date_text = date_text_element.text.strip()
                date_str = date_text.split(" ")[0]
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    continue  # 날짜 변환 실패 시 다음 루프로
            else:
                continue  # 날짜 요소가 없으면 다음 루프로

            team_1 = soup.select_one(
                "body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child(1) > td:nth-child(1) > a"
            ).text.strip()  # 팀 1 이름
            team_2 = soup.select_one(
                "body > div.warp > div.container > section > div:nth-child(4) > div > div > div > div.box_cont > div.table_type03 > table > tbody > tr:nth-child(2) > td:nth-child(1) > a"
            ).text.strip()  # 팀 2 이름

            # 중복 체크 (날짜, 팀 1, 팀 2 조합 확인)
            if GameRecord.objects.filter(
                date=date, team_1=team_1, team_2=team_2
            ).exists():
                print(f"중복된 레코드 발견: {date}, {team_1} vs {team_2}. 건너뜁니다.")
                continue  # 중복된 경우 건너뜀

            # GameRecord 모델에 데이터 저장
            game_record = GameRecord(
                date=date,  # 날짜
                team_1=team_1,  # 팀 1 이름
                team_2=team_2,  # 팀 2 이름
                inning_scores_team_1=inning_scores_team_1,  # 팀 1 이닝 점수
                inning_scores_team_2=inning_scores_team_2,  # 팀 2 이닝 점수
                r_h_e_b_team_1=r_h_e_b_team_1,
                r_h_e_b_team_2=r_h_e_b_team_2,
            )
            game_record.save()  # 데이터베이스에 저장
            total_records += 1  # 레코드 수 증가

    return total_records
