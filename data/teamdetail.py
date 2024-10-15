import requests
from bs4 import BeautifulSoup
from .models import TeamDetail  # 모델 import


def fetch_teamdetail_data():
    """팀 통계 데이터를 크롤링하여 데이터베이스에 저장"""
    url = "https://statiz.sporki.com/stats/?m=team"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # 팀 이름과 팀 번호 매핑
    team_numbers = {
        "KIA": "2002",
        "두산": "6002",
        "롯데": "3001",
        "NC": "11001",
        "키움": "10001",
        "삼성": "1001",
        "한화": "7002",
        "KT": "12001",
        "SSG": "9002",
        "LG": "5002",
    }

    # 두 번째 테이블 선택
    tables = soup.find_all("table")  # 모든 테이블 선택
    if len(tables) < 2:
        raise Exception("두 번째 테이블을 찾을 수 없습니다.")

    table = tables[1]  # 두 번째 테이블

    rows = table.find_all("tr")
    if not rows:
        raise Exception("행을 찾을 수 없습니다.")

    total_records = 0  # 저장된 레코드 수

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 32:  # 모든 필요한 데이터 열이 있는지 확인
            try:
                team = cols[1].text.strip()  # 팀 이름
                year = float(cols[2].text.strip())  # 연도
                war = float(cols[3].text.strip())  # WAR
                owar = float(cols[4].text.strip())  # oWAR
                dwar = float(cols[5].text.strip())  # dWAR
                g = float(cols[6].text.strip())  # G
                pa = float(cols[7].text.strip())  # PA
                epa = float(cols[8].text.strip())  # ePA
                ab = float(cols[9].text.strip())  # AB
                r = float(cols[10].text.strip())  # R
                h = float(cols[11].text.strip())  # H
                two_b = float(cols[12].text.strip())  # 2B
                three_b = float(cols[13].text.strip())  # 3B
                hr = float(cols[14].text.strip())  # HR
                tb = float(cols[15].text.strip())  # TB
                rbi = float(cols[16].text.strip())  # RBI
                sb = float(cols[17].text.strip())  # SB
                cs = float(cols[18].text.strip())  # CS
                bb = float(cols[19].text.strip())  # BB
                hp = float(cols[20].text.strip())  # HP
                ib = float(cols[21].text.strip())  # IB
                so = float(cols[22].text.strip())  # SO
                gdp = float(cols[23].text.strip())  # GDP
                sh = float(cols[24].text.strip())  # SH
                sf = float(cols[25].text.strip())  # SF
                avg = (
                    float(cols[26].text.strip()) if cols[26].text.strip() else 0.0
                )  # AVG
                obp = (
                    float(cols[27].text.strip()) if cols[27].text.strip() else 0.0
                )  # OBP
                slg = (
                    float(cols[28].text.strip()) if cols[28].text.strip() else 0.0
                )  # SLG
                ops = (
                    float(cols[29].text.strip()) if cols[29].text.strip() else 0.0
                )  # OPS
                re_pa = (
                    float(cols[30].text.strip()) if cols[30].text.strip() else 0.0
                )  # R/ePA
                wrc_plus = (
                    float(cols[31].text.strip()) if cols[31].text.strip() else 0.0
                )  # wRC+

                # 팀 넘버 가져오기
                team_number = team_numbers.get(team, "")  # 팀 이름으로 팀 넘버 가져오기

                # 데이터베이스에 저장 (rank는 제거하고 team을 먼저 지정)
                TeamDetail.objects.update_or_create(
                    team=team,  # 팀 이름을 먼저 지정
                    year=year,
                    defaults={
                        "team_number": team_number,  # 팀 넘버 추가
                        "war": war,
                        "owar": owar,
                        "dwar": dwar,
                        "games": g,
                        "plate_appearances": pa,
                        "effective_pa": epa,
                        "at_bats": ab,
                        "runs": r,
                        "hits": h,
                        "two_b": two_b,
                        "three_b": three_b,
                        "home_runs": hr,
                        "total_bases": tb,
                        "rbi": rbi,
                        "stolen_bases": sb,
                        "caught_stealing": cs,
                        "walks": bb,
                        "hit_by_pitch": hp,
                        "intentional_walks": ib,
                        "strikeouts": so,
                        "grounded_into_double_play": gdp,
                        "sacrifice_hits": sh,
                        "sacrifice_flies": sf,
                        "batting_average": avg,
                        "on_base_percentage": obp,
                        "slugging_percentage": slg,
                        "on_base_plus_slugging": ops,
                        "runs_per_effective_pa": re_pa,
                        "wrc_plus": wrc_plus,
                    },
                )
                total_records += 1  # 레코드 저장 시 카운트 증가

            except ValueError as e:
                print(f"데이터 변환 오류: {e}, row: {row.text}")
            except Exception as e:
                print(f"오류 발생: {e}")

    print(f"총 {total_records}개의 팀 기록이 저장되었습니다.")
    return total_records
