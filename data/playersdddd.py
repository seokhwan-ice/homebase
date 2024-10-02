# # import os
# # import time
# # import django
# # from selenium import webdriver
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from django.db import IntegrityError
# #
# # from data.models import PlayerRecord
# #
# # # Django 설정 초기화
# # os.environ.setdefault(
# #     "DJANGO_SETTINGS_MODULE", "homebase.settings"
# # )  # 프로젝트 이름 수정
# # django.setup()
# #
# # # Chrome 옵션 설정
# # chrome_options = Options()
# # # chrome_options.add_argument("--headless")  # 헤드리스 모드
# # chrome_options.add_argument("--no-sandbox")
# # chrome_options.add_argument("--disable-dev-shm-usage")
# # chrome_options.add_argument(
# #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# # )
# # chrome_options.add_argument("--ignore-certificate-errors")
# #
# #
# # # WebDriver 경로 설정
# # driver_path = "C:\\Users\\Win10\\Desktop\\HomeBase\\homebase\\data\\chromedriver.exe"
# # service = Service(driver_path)
# # ### 시도횟수 대기시간 조절하면 됨 대충 100초
# #
# # # # 포문돌리기
# # # # driver = webdriver.Chrome(service=service, options=chrome_options)
# # #
# # # 팀명 리스트 설정
# # t_names = ["해태+KIA"]  # 팀명을 적절히 수정하세요
# #
# #
# # def fetch_team_players():
# #     # 팀 페이지 URL로 이동
# #     team_url = (
# #         "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=2002&year=2024"
# #     )
# #
# #     with webdriver.Chrome(service=service, options=chrome_options) as driver:
# #         driver.get(team_url)
# #
# #         # 선수 목록 가져오기
# #         player_elements = driver.find_elements(
# #             By.CSS_SELECTOR, "a[href*='playerinfo']"
# #         )  # playerinfo가 포함된 a 태그 선택
# #
# #         for player_element in player_elements:
# #             player_name = player_element.text.strip()
# #             player_link = player_element.get_attribute(
# #                 "href"
# #             )  # 선수 페이지 링크 가져오기
# #
# #             # 선수 페이지로 이동
# #             driver.get(player_link)
# #
# #             # 최종적으로 접근해야 할 URL 로직 (예시)
# #             p_no = player_link.split("p_no=")[-1]  # p_no 추출
# #             final_url = f"https://statiz.sporki.com/player/?m=playerinfo&p_no={p_no}"
# #             print(f"Accessing final URL: {final_url}")
# #
# #             # 선수 데이터 수집 후, 팀 페이지로 돌아가기
# #             driver.get(team_url)
# #             WebDriverWait(driver, 10).until(
# #                 EC.presence_of_element_located(
# #                     (By.CSS_SELECTOR, "a[href*='playerinfo']")
# #                 )
# #             )
# #             time.sleep(5)  # 너무 짧은 대기는 피할 수 있으므로 약간의 여유 시간 추가
# #
# #
# # # 예시로 팀 코드 2002를 사용
# # fetch_team_players()
# #
# #
# # # 241001
# # # 팀명에서 클릭보다 선수 이름으로 태그 잡아서 들어가기
# # # 팀명 :  t_name 리스트로 받아놓고 시작... ["해티+KIA", "OB+두산"] 이런느낌으로...
# # # 등번호 ;  p_num (클릭으로)
# # # 선수체크 :  <a href="/player/?m=playerinfo&amp;p_no=15435">곽도규</a> 텍스트로 '텍스트' 입력	.send_keys('') (텍스트로 찾게)
# # # 상대별 눌러서 가져오기 :  <a href="/player/?m=rival&amp;p_no=15435" class="p_match">상대별</a> (클릭으로)
# # # 이 테이블의 자료 가져오기 :  <div class="table_type02 transverse_scroll cbox"> (크롤링 슈루룩)
# #
# # # -> 코드 다시 짜기
# # # 트러블
# #
# # # 데이터를 가져오지 않는다 어떻게??? 서버나 이런거에서는 오류가 나지 않음... postman에서도 정상 작동
# # # 왜그런지 찾아봐야함
#
# import os
# import django
# import logging
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
# from django.db import IntegrityError
# from setuptools.installer import fetch_build_egg
#
# from data.models import PlayerRecord, RivalStats
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
# chrome_options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# )
# chrome_options.add_argument("--ignore-certificate-errors")
#
# # WebDriver 경로 설정
# driver_path = "C:\\Users\\Win10\\Desktop\\HomeBase\\homebase\\data\\chromedriver.exe"
# service = Service(driver_path)
#
# # 팀 페이지 URL
# team_url = "https://statiz.sporki.com/team/?m=team&t_code=2002&year=2024"
#
#
# def safe_int(value):
#     """문자열을 정수로 변환, 실패 시 0 반환"""
#     try:
#         return int(value)
#     except ValueError:
#         return 0
#
#
# # 플레이어 스텟 = 상대 전적을 모두 더한 것으로
# # 선수 프로필??
#
#
# ######################################### 이부분이 에러나는중 데이터 수집이 똑바로 안됨. 여기는 프로필로 수정
# def fetch_stats(url, driver):
#     """주어진 URL에서 통계를 가져오는 함수"""
#     try:
#         driver.get(url)
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
#         )
#
#         rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
#         stats = []
#         for row in rows:
#             cols = row.find_elements(By.TAG_NAME, "td")
#             if len(cols) >= 24:
#                 player_name_element = row.find_element(By.CSS_SELECTOR, "td a")
#                 player_name = (
#                     player_name_element.text.strip()
#                     if player_name_element
#                     else "Unknown"
#                 )
#
#                 stat = {
#                     "player_name": player_name,
#                     "player_link": url,
#                     "pa": safe_int(cols[1].text),
#                     "epa": safe_int(cols[2].text),
#                     "ab": safe_int(cols[3].text),
#                     "r": safe_int(cols[4].text),
#                     "h": safe_int(cols[5].text),
#                     "two_b": safe_int(cols[6].text),
#                     "three_b": safe_int(cols[7].text),
#                     "hr": safe_int(cols[8].text),
#                     "tb": safe_int(cols[9].text),
#                     "rbi": safe_int(cols[10].text),
#                     "bb": safe_int(cols[11].text),
#                     "hp": safe_int(cols[12].text),
#                     "ib": safe_int(cols[13].text),
#                     "so": safe_int(cols[14].text),
#                     "gdp": safe_int(cols[15].text),
#                     "sh": safe_int(cols[16].text),
#                     "sf": safe_int(cols[17].text),
#                     "avg": float(cols[18].text) if cols[18].text else 0.0,
#                     "obp": float(cols[19].text) if cols[19].text else 0.0,
#                     "slg": float(cols[20].text) if cols[20].text else 0.0,
#                     "ops": float(cols[21].text) if cols[21].text else 0.0,
#                     "np": safe_int(cols[22].text),
#                     "avli": float(cols[23].text) if cols[23].text else 0.0,
#                     "re24": float(cols[24].text) if cols[24].text else 0.0,
#                     "wpa": float(cols[25].text) if cols[25].text else 0.0,
#                 }
#                 stats.append(stat)
#         logging.info(f"수집된 통계 데이터: {stats}")
#         return stats  # 모든 선수의 통계를 반환
#     except TimeoutException:
#         logging.error("Timeout while fetching stats from URL: %s", url)
#     except StaleElementReferenceException:
#         logging.warning("Stale element reference while fetching stats.")
#     except Exception as e:
#         logging.error(f"Error fetching stats from {url}: {str(e)}")
#     return []
#
#
# def fetch_rival_stats(url, driver):
#     try:
#         # 페이지 로드
#         driver.get(url)
#         logging.info(f"Fetching rival stats from URL: {url}")
#
#         WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located(
#                 (By.CSS_SELECTOR, "div.table_type02.transverse_scroll.cbox table")
#             )
#         )
#
#         # 테이블의 행을 가져옴
#         rows = driver.find_elements(
#             By.CSS_SELECTOR, "div.table_type02.transverse_scroll.cbox table tbody tr"
#         )
#         logging.info(
#             f"Found {len(rows)} rows in the rival stats table."
#         )  # 테이블의 행 개수를 로그로 출력
#
#         # 수집된 통계 데이터를 저장할 리스트
#         rival_stats = []
#
#         # 각 행의 데이터 추출
#         for row in rows:
#             cols = row.find_elements(By.TAG_NAME, "td")
#             if len(cols) > 1:  # 각 열에 데이터가 있는지 확인
#                 rival_name = cols[0].text.strip()  # 상대 선수 이름
#                 pa = safe_int(cols[1].text)  # 타석
#                 ab = safe_int(cols[2].text)  # 타수
#                 h = safe_int(cols[3].text)  # 안타
#                 hr = safe_int(cols[4].text)  # 홈런
#                 rbi = safe_int(cols[5].text)  # 타점
#                 avg = float(cols[6].text) if cols[6].text else 0.0  # 타율
#
#                 # 데이터 딕셔너리 생성
#                 stat = {
#                     "rival_name": rival_name,
#                     "pa": pa,
#                     "ab": ab,
#                     "h": h,
#                     "hr": hr,
#                     "rbi": rbi,
#                     "avg": avg,
#                 }
#                 rival_stats.append(stat)
#
#         logging.info(f"수집된 상대 선수 통계 데이터: {rival_stats}")
#         return rival_stats  # 모든 상대 선수의 통계 반환
#     except TimeoutException:
#         logging.error("Timeout while fetching rival stats from URL: %s", url)
#     except StaleElementReferenceException:
#         logging.warning("Stale element reference while fetching rival stats.")
#     except Exception as e:
#         logging.error(f"Error fetching rival stats from {url}: {str(e)}")
#     return []
#
#
# def save_records(records):
#     """모든 선수 통계를 데이터베이스에 저장하는 함수"""
#     for record in records:
#         try:
#             logging.info(f"저장할 선수 이름: {record['player_name']}")
#             player_stat = PlayerRecord(
#                 player_name=record["player_name"],
#                 player_link=record["player_link"],
#                 pa=record["pa"],
#                 epa=record["epa"],
#                 ab=record["ab"],
#                 r=record["r"],
#                 h=record["h"],
#                 two_b=record["two_b"],
#                 three_b=record["three_b"],
#                 hr=record["hr"],
#                 tb=record["tb"],
#                 rbi=record["rbi"],
#                 bb=record["bb"],
#                 hp=record["hp"],
#                 ib=record["ib"],
#                 so=record["so"],
#                 gdp=record["gdp"],
#                 sh=record["sh"],
#                 sf=record["sf"],
#                 avg=record["avg"],
#                 obp=record["obp"],
#                 slg=record["slg"],
#                 ops=record["ops"],
#                 np=record["np"],
#                 avli=record["avli"],
#                 re24=record["re24"],
#                 wpa=record["wpa"],
#             )
#             player_stat.save()
#         except IntegrityError as e:
#             logging.error(
#                 f"Failed to save record for {record['player_name']}: {str(e)}"
#             )
#
#
# def save_rival_stats(records):
#     for record in records:
#         try:
#             rival_stat = RivalStats(
#                 rival_name=record["rival_name"],
#                 pa=record["pa"],
#                 ab=record["ab"],
#                 h=record["h"],
#                 hr=record["hr"],
#                 rbi=record["rbi"],
#                 avg=record["avg"],
#             )
#             rival_stat.save()
#             logging.info(f"Saved rival stats for {record['rival_name']}")
#         except IntegrityError as e:
#             logging.error(f"Failed to save record for {record['rival_name']}: {str(e)}")
#
#
# ### 삭제 금지###
# def fetch_team_players():
#     driver = None
#     all_player_stats = []  # 모든 선수 통계를 저장할 리스트
#     all_rival_stats = []  # 모든 상대 선수 전적을 저장할 리스트
#     try:
#         driver = webdriver.Chrome(service=service, options=chrome_options)
#         driver.get(team_url)
#
#         # 시즌 백넘버 페이지로 이동
#         season_backnumber_url = (
#             "https://statiz.sporki.com/team/?m=seasonBacknumber&t_code=2002&year=2024"
#         )
#         driver.get(season_backnumber_url)
#
#         while True:
#             player_elements = WebDriverWait(driver, 10).until(
#                 EC.presence_of_all_elements_located(
#                     (By.CSS_SELECTOR, "a[href*='playerinfo']")
#                 )
#             )
#
#             for player_element in player_elements:
#                 try:
#                     player_name = player_element.text.strip()
#                     player_link = player_element.get_attribute("href")
#
#                     # 선수 통계 가져오기
#                     player_stats = fetch_stats(player_link, driver)
#                     # 이게 실행한 결과가 아래@@@@
#                     # 로그로 데이터 확인
#                     logging.info(
#                         f"{player_name}의 통계 수집 완료. 데이터: {player_stats}"
#                     )
#                     ####### 여기가 비어서 나오는중@@@
#
#                     # 수집한 통계가 있는지 확인 후 리스트에 추가
#                     if player_stats:
#                         for stat in player_stats:
#                             stat["player_name"] = player_name
#                             stat["player_link"] = player_link
#                             all_player_stats.append(stat)  # 수집한 통계를 리스트에 추가
#
#                     logging.info(f"{player_name}의 통계를 성공적으로 수집했습니다.")
#
#                     # rival 페이지 URL 변경
#                     rival_link = player_link.replace("playerinfo", "rival")
#                     logging.info(
#                         f"Fetching rival stats for {player_name} from {rival_link}"
#                     )
#
#                     # 상대 선수 전적 가져오기
#                     rival_stats = fetch_rival_stats(rival_link, driver)
#                     if rival_stats:
#                         for stat in rival_stats:
#                             stat["player_name"] = player_name  # 주 선수 이름 추가
#                             all_rival_stats.append(
#                                 stat
#                             )  # 상대 선수 전적을 리스트에 추가
#
#                     logging.info(f"{player_name}의 상대 선수 전적 수집 완료.")
#                 except StaleElementReferenceException:
#                     logging.warning(
#                         "StaleElementReferenceException 발생, 다시 시도합니다."
#                     )
#                     continue
#     finally:
#         if driver:
#             driver.quit()
#
#         # 통계가 잘 수집되었는지 확인
#         logging.info(f"수집된 선수 통계의 개수: {len(all_player_stats)}")
#         logging.info(f"수집된 상대 선수 전적의 개수: {len(all_rival_stats)}")
#
#         # 모든 선수 통계를 한 번에 저장
#         save_records(all_player_stats)
#         save_rival_stats(all_rival_stats)  # 상대 선수 전적 저장
#
#
# #### 삭제 금지####
#
#
# if __name__ == "__main__":
#     fetch_team_players()
#
# # import os
# # import django
# # import logging
# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from django.db import IntegrityError
# # from data.models import RivalStats  # RivalStats 모델 임포트
# #
# # # Django 설정 초기화
# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homebase.settings")
# # django.setup()
# #
# # # 로깅 설정
# # logging.basicConfig(level=logging.DEBUG)
# #
# # # Chrome 옵션 설정
# # chrome_options = Options()
# # chrome_options.add_argument("--no-sandbox")
# # chrome_options.add_argument("--disable-dev-shm-usage")
# # chrome_options.add_argument("--headless")  # 브라우저가 보이지 않게 설정
# # chrome_options.add_argument(
# #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# # )
# #
# # # WebDriver 경로 설정
# # driver_path = "C:\\Users\\Win10\\Desktop\\HomeBase\\homebase\\data\\chromedriver.exe"
# # service = Service(driver_path)
# #
# #
# # # playersdddd.py
# # def fetch_team_players():
# #     # 함수 내용
# #     pass
