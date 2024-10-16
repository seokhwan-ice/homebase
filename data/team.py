import requests
from bs4 import BeautifulSoup
from .models import TeamRecord  # 모델 import


def fetch_team_data():
    # 각 팀의 고유 팀 넘버, 팀 이름 및 URL 정의
    urls = [
        (
            "2002",
            "기아",
            "https://statiz.sporki.com/team/?m=team&t_code=2002&year=2024",
        ),  # 기아
        (
            "6002",
            "두산",
            "https://statiz.sporki.com/team/?m=team&t_code=6002&year=2024",
        ),  # 두산
        (
            "3001",
            "롯데",
            "https://statiz.sporki.com/team/?m=team&t_code=3001&year=2024",
        ),  # 롯데
        (
            "11001",
            "NC",
            "https://statiz.sporki.com/team/?m=team&t_code=11001&year=2024",
        ),  # NC
        (
            "10001",
            "키움",
            "https://statiz.sporki.com/team/?m=team&t_code=10001&year=2024",
        ),  # 키움
        (
            "1001",
            "삼성",
            "https://statiz.sporki.com/team/?m=team&t_code=1001&year=2024",
        ),  # 삼성
        (
            "7002",
            "한화",
            "https://statiz.sporki.com/team/?m=team&t_code=7002&year=2024",
        ),  # 한화
        (
            "12001",
            "KT",
            "https://statiz.sporki.com/team/?m=team&t_code=12001&year=2024",
        ),  # KT
        (
            "9002",
            "SSG",
            "https://statiz.sporki.com/team/?m=team&t_code=9002&year=2024",
        ),  # SSG
        (
            "5002",
            "LG",
            "https://statiz.sporki.com/team/?m=team&t_code=5002&year=2024",
        ),  # LG
    ]

    total_records = 0  # 저장된 레코드 수

    for team_number, team_name, url in urls:
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error fetching {url}: {response.status_code}")
            continue  # 다음 URL로 넘어감

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.select_one(
            "body > div.warp > div.container > section > div.top_meum_box > div.box_type_boared02 > div:nth-child(2) > div:nth-child(2) > div > div > div.box_cont > div > table"
        )

        if not table:
            print(f"Table not found in {url}.")
            continue  # 다음 URL로 넘어감

        rows = table.find_all("tr")

        # 첫 번째 행은 헤더이므로 두 번째 행부터 시작
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) == 5:  # 데이터가 있는 열만 처리
                rival = cols[0].text.strip()  # 라이벌 팀 이름
                wins = int(cols[1].text.strip())
                draws = int(cols[2].text.strip())
                losses = int(cols[3].text.strip())
                win_rate = float(
                    cols[4].text.strip().replace("%", "")
                )  # % 제거 후 float로 변환

                # 데이터베이스에 저장
                TeamRecord.objects.update_or_create(
                    team_name=team_name,
                    rival=rival,
                    team_number=team_number,  # 팀 넘버를 여기에 추가
                    defaults={
                        "wins": wins,
                        "draws": draws,
                        "losses": losses,
                        "win_rate": win_rate,  # 100으로 나누지 않음
                    },
                )
                total_records += 1  # 성공적으로 저장된 레코드 수 증가

    print(f"총 {total_records}개의 레코드가 저장되었습니다.")
    return total_records  # 저장된 레코드 수 반환
