import requests
from bs4 import BeautifulSoup
from data.models import PlayerRecord  # 모델 임포트


# 안전하게 float 변환하는 함수
def safe_convert_to_float(value):
    try:
        return float(value) if value else 0.0
    except ValueError:
        return 0.0  # 변환할 수 없을 때 기본값


# 안전하게 int 변환하는 함수
def safe_convert_to_int(value):
    try:
        return int(value) if value else 0
    except ValueError:
        return 0  # 변환할 수 없을 때 기본값


def crawl_playerrival_data():
    # 각 팀의 URL을 리스트로 저장
    base_url = "https://statiz.sporki.com"
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

    # 각 팀에 대한 로고 URL을 저장
    team_logos = {
        "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=2002&year=2024": "https://statiz.sporki.com/data/team/ci/2024/2002.svg",  # 기아타이거즈
        "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=6002&year=2024": "https://statiz.sporki.com/data/team/ci/2024/6002.svg",  # 두산베어스
        "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=3001&year=2024": "https://statiz.sporki.com/data/team/ci/2024/3001.svg",  # 롯데자이언츠
        "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=11001&year=2024": "https://statiz.sporki.com/data/team/ci/2024/11001.svg",  # NC다이노스
        "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=10001&year=2024": "https://statiz.sporki.com/data/team/ci/2024/10001.svg",  # 키움히어로즈
        "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=1001&year=2024": "https://statiz.sporki.com/data/team/ci/2024/1001.svg",  # 삼성라이온즈
        "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=7002&year=2024": "https://statiz.sporki.com/data/team/ci/2024/7002.svg",  # 한화이글스
        "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=12001&year=2024": "https://statiz.sporki.com/data/team/ci/2024/12001.svg",  # KT위즈
        "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=9002&year=2024": "https://statiz.sporki.com/data/team/ci/2024/9002.svg",  # SSG랜더스
        "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=5002&year=2024": "https://statiz.sporki.com/data/team/ci/2024/5002.svg",  # LG트윈스
    }

    for url in team_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # 클래스가 'uniform'인 모든 div 태그 선택
        uniform_divs = soup.find_all("div", class_="uniform")

        # 각 uniform div에서 a 태그의 href와 텍스트 저장
        for div in uniform_divs:
            a_tags = div.find_all("a")
            for a in a_tags:
                # href에서 playerinfo 값을 rival로 변경
                href_value = a["href"].replace("playerinfo", "rival")

                # 상대 경로를 절대 경로로 변경
                player_url = f"{base_url}{href_value}"

                # 선수 넘버 추출 (player_url에서 p_no 값을 추출)
                player_number = player_url.split("p_no=")[-1]  # URL에서 선수 넘버 추출

                # 선수의 rival 페이지에서 테이블 내용 크롤링
                player_response = requests.get(player_url)
                player_soup = BeautifulSoup(player_response.text, "html.parser")

                # 'table' 클래스를 가진 테이블을 선택
                table = player_soup.find("table")

                # 팀 URL에 해당하는 로고 URL 가져오기
                team_logo = team_logos.get(url, "")

                # 테이블의 내용을 리스트로 저장
                if table:
                    rows = table.find_all("tr")[1:]
                    for row in rows:
                        cols = row.find_all("td")
                        cols = [ele.text.strip() for ele in cols]

                        # opponent 값이 비어 있으면 건너뛰기
                        if not cols or not cols[0]:
                            continue  # opponent 값이 없으면 건너뜀

                        # 데이터베이스에 저장 (중복 확인)
                        player_record, created = PlayerRecord.objects.get_or_create(
                            name=f"{a.text}",  # 팀 로고와 선수 이름 결합
                            opponent=cols[0] if len(cols) > 0 else "",  # 상대 이름
                            defaults={
                                "player_number": player_number,
                                "team_logo_url": team_logo,  # 팀 로고 URL
                                "pa": (
                                    safe_convert_to_int(cols[1]) if len(cols) > 1 else 0
                                ),  # PA
                                "epa": (
                                    safe_convert_to_int(cols[2]) if len(cols) > 2 else 0
                                ),  # ePA
                                "ab": (
                                    safe_convert_to_int(cols[3]) if len(cols) > 3 else 0
                                ),  # AB
                                "r": (
                                    safe_convert_to_int(cols[4]) if len(cols) > 4 else 0
                                ),  # R
                                "h": (
                                    safe_convert_to_int(cols[5]) if len(cols) > 5 else 0
                                ),  # H
                                "two_b": (
                                    safe_convert_to_int(cols[6]) if len(cols) > 6 else 0
                                ),  # 2B
                                "three_b": (
                                    safe_convert_to_int(cols[7]) if len(cols) > 7 else 0
                                ),  # 3B
                                "hr": (
                                    safe_convert_to_int(cols[8]) if len(cols) > 8 else 0
                                ),  # HR
                                "tb": (
                                    safe_convert_to_int(cols[9]) if len(cols) > 9 else 0
                                ),  # TB
                                "rbi": (
                                    safe_convert_to_int(cols[10])
                                    if len(cols) > 10
                                    else 0
                                ),  # RBI
                                "bb": (
                                    safe_convert_to_int(cols[11])
                                    if len(cols) > 11
                                    else 0
                                ),  # BB
                                "hp": (
                                    safe_convert_to_int(cols[12])
                                    if len(cols) > 12
                                    else 0
                                ),  # HP
                                "ib": (
                                    safe_convert_to_int(cols[13])
                                    if len(cols) > 13
                                    else 0
                                ),  # IB
                                "so": (
                                    safe_convert_to_int(cols[14])
                                    if len(cols) > 14
                                    else 0
                                ),  # SO
                                "gdp": (
                                    safe_convert_to_int(cols[15])
                                    if len(cols) > 15
                                    else 0
                                ),  # GDP
                                "sh": (
                                    safe_convert_to_int(cols[16])
                                    if len(cols) > 16
                                    else 0
                                ),  # SH
                                "sf": (
                                    safe_convert_to_int(cols[17])
                                    if len(cols) > 17
                                    else 0
                                ),  # SF
                                "avg": (
                                    safe_convert_to_float(cols[18])
                                    if len(cols) > 18
                                    else 0.0
                                ),  # AVG
                                "obp": (
                                    safe_convert_to_float(cols[19])
                                    if len(cols) > 19
                                    else 0.0
                                ),  # OBP
                                "slg": (
                                    safe_convert_to_float(cols[20])
                                    if len(cols) > 20
                                    else 0.0
                                ),  # SLG
                                "ops": (
                                    safe_convert_to_float(cols[21])
                                    if len(cols) > 21
                                    else 0.0
                                ),  # OPS
                                "np": (
                                    safe_convert_to_int(cols[22])
                                    if len(cols) > 22
                                    else 0
                                ),  # NP
                                "avli": (
                                    safe_convert_to_float(cols[23])
                                    if len(cols) > 23
                                    else 0.0
                                ),  # avLI
                                "re24": (
                                    safe_convert_to_float(cols[24])
                                    if len(cols) > 24
                                    else 0.0
                                ),  # RE24
                                "wpa": (
                                    safe_convert_to_float(cols[25])
                                    if len(cols) > 25
                                    else 0.0
                                ),  # WPA
                            },
                        )

                        # 새로 생성된 경우에만 로그 출력
                        if created:
                            print(
                                f"Created record for {player_record.name} against {player_record.opponent}."
                            )
                        else:
                            print(
                                f"Record already exists for {player_record.name} against {player_record.opponent}."
                            )

    # 결과 출력
    return PlayerRecord.objects.count()
