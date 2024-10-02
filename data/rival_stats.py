# import os
# import django
# import logging
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from django.db import IntegrityError
# from data.models import RivalStats  # RivalStats 모델 임포트
#
# # Django 설정 초기화
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homebase.settings")
# django.setup()
#
# # 로깅 설정
# logging.basicConfig(level=logging.DEBUG)
#
# # Chrome 옵션 설정
# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--headless")  # 브라우저가 보이지 않게 설정
# chrome_options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# )
#
# # WebDriver 경로 설정
# driver_path = "C:\\Users\\Win10\\Desktop\\HomeBase\\homebase\\data\\chromedriver.exe"
# service = Service(driver_path)
#
#
# def fetch_and_save_rival_stats(player_no):
#     """주어진 선수 번호에 대한 라이벌 통계를 가져와서 데이터베이스에 저장하는 함수"""
#     rival_stats_url = f"https://statiz.sporki.com/player/?m=rival&p_no={player_no}"
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#
#     try:
#         driver.get(rival_stats_url)
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "div.table_type02"))
#         )
#
#         # 모든 행(row) 가져오기
#         rows = driver.find_elements(By.CSS_SELECTOR, "div.table_type02 tbody tr")
#         for row in rows:
#             cols = row.find_elements(By.TAG_NAME, "td")
#             if len(cols) >= 23:  # 필요한 열 수 확인
#                 try:
#                     rival_stat = RivalStats(
#                         rival_name=cols[1].text.strip(),  # 라이벌 선수 이름
#                         plate_appearances=int(cols[2].text.strip()),  # PA
#                         effective_plate_appearances=int(cols[3].text.strip()),  # ePA
#                         at_bats=int(cols[4].text.strip()),  # AB
#                         runs=int(cols[5].text.strip()),  # R
#                         hits=int(cols[6].text.strip()),  # H
#                         doubles=int(cols[7].text.strip()),  # 2B
#                         triples=int(cols[8].text.strip()),  # 3B
#                         home_runs=int(cols[9].text.strip()),  # HR
#                         total_bases=int(cols[10].text.strip()),  # TB
#                         rbis=int(cols[11].text.strip()),  # RBI
#                         walks=int(cols[12].text.strip()),  # BB
#                         hit_by_pitch=int(cols[13].text.strip()),  # HP
#                         intentional_walks=int(cols[14].text.strip()),  # IB
#                         strikeouts=int(cols[15].text.strip()),  # SO
#                         grounded_into_double_play=int(cols[16].text.strip()),  # GDP
#                         sacrifice_hits=int(cols[17].text.strip()),  # SH
#                         sacrifice_flies=int(cols[18].text.strip()),  # SF
#                         batting_average=(
#                             float(cols[19].text.strip())
#                             if cols[19].text.strip()
#                             else 0.0
#                         ),  # AVG
#                         on_base_percentage=(
#                             float(cols[20].text.strip())
#                             if cols[20].text.strip()
#                             else 0.0
#                         ),  # OBP
#                         slugging_percentage=(
#                             float(cols[21].text.strip())
#                             if cols[21].text.strip()
#                             else 0.0
#                         ),  # SLG
#                         ops=(
#                             float(cols[22].text.strip())
#                             if cols[22].text.strip()
#                             else 0.0
#                         ),  # OPS
#                         pitches=(
#                             int(cols[23].text.strip()) if cols[23].text.strip() else 0
#                         ),  # NP
#                         average_leverage_index=(
#                             float(cols[24].text.strip())
#                             if cols[24].text.strip()
#                             else 0.0
#                         ),  # avLI
#                         re24=(
#                             float(cols[25].text.strip())
#                             if cols[25].text.strip()
#                             else 0.0
#                         ),  # RE24
#                         wpa=(
#                             float(cols[26].text.strip())
#                             if cols[26].text.strip()
#                             else 0.0
#                         ),  # WPA
#                     )
#                     rival_stat.save()  # 데이터베이스에 저장
#                     logging.info(f"Saved rival stat for {rival_stat.rival_name}")
#                 except IntegrityError:
#                     logging.warning(
#                         f"Duplicate entry for {cols[1].text.strip()}"
#                     )  # 중복 데이터 처리
#                 except Exception as e:
#                     logging.error(
#                         f"Error saving data for {cols[1].text.strip()}: {str(e)}"
#                     )
#
#     except Exception as e:
#         logging.error(f"Error fetching rival stats for player {player_no}: {str(e)}")
#     finally:
#         driver.quit()
#

# # 예시: 곽도규 선수의 라이벌 통계 가져오기 및 저장
# player_number = 15435
# fetch_and_save_rival_stats(player_number)
