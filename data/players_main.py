# # #### 절대 삭제 금지###
# # ### 해야할거
# # ### 데이터 베이스 저장하는법 데이터 형태 잘 생각해서 저장하기!!!
# # ### 전체 페이지(2. 팀별 반복문 돌리기)
# # ### 모델정의
# # ### 유니폼 a태그 값에 href가 있음.
import requests
from bs4 import BeautifulSoup

# 선수 목록을 가져오는 URL
base_url = "https://statiz.sporki.com"
url = f"{base_url}/team/?m=seasonBacknumber&t_code=2002&year=2024"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 클래스가 'uniform'인 모든 div 태그 선택
uniform_divs = soup.find_all("div", class_="uniform")

# 선수 데이터를 저장할 딕셔너리
player_data = {}

# 각 uniform div에서 a 태그의 href와 텍스트 저장
for div in uniform_divs:
    a_tags = div.find_all("a")
    for a in a_tags:
        # href에서 playerinfo 값을 rival로 변경
        href_value = a["href"].replace("playerinfo", "rival")

        # 상대 경로를 절대 경로로 변경
        player_url = f"{base_url}{href_value}"

        # 선수의 rival 페이지에서 테이블 내용 크롤링
        player_response = requests.get(player_url)
        player_soup = BeautifulSoup(player_response.text, "html.parser")

        # 예를 들어, 'table'이라는 클래스를 가진 테이블을 찾는다고 가정
        table = player_soup.find(
            "table"
        )  # 적절한 선택자를 사용하여 원하는 테이블을 선택하세요

        # 테이블의 내용을 리스트로 저장
        if table:
            rows = table.find_all("tr")
            table_data = []
            for row in rows:
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                if cols:  # 빈 리스트는 저장하지 않음
                    table_data.append(cols)

            # 딕셔너리에 저장
            player_data[a.text] = table_data

# 결과 출력
print(player_data)
