import schedule
import time
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from data.crawling import get_content


from openai_test import summery_article

# schedule.every().day.do()

# 1번 파일이 실행될 때 환경변수에 현재 자신의 프로젝트의 settings.py파일 경로를 등록.
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIBI_NEWS.settings")

# 2번 실행파일에 Django 환경을 불러오는 작업.
import django

django.setup()
from posts.models import Headline


# 네이버 헤드라인 뉴스의 url 가져오기
def get_urls():
    # 크롬 드라이버 옵션
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")  # 새 창 없는 모드
    chrome_options.add_experimental_option(
        "detach", True
    )  # 드라이버에 종료 명령이 없으면 브라우저를 끄지 않음
    chrome_options.add_argument("lang=ko_KR")  # 한국어
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://news.naver.com/section/105"

    driver.get(url)
    driver.implicitly_wait(3)  # 3초 대기

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

    context = {
        "titles": [],
        "urls": [],
    }

    test = soup.find_all("a", "sa_text_title")
    for i in range(5):
        t = test[i]
        context["titles"].append(t.get_text(strip=True))
        context["urls"].append((t.get("href")))

    driver.quit()
    return context


def headline_summary():
    headlines = get_urls()
    head_urls = headlines.get("urls")
    for i, url in enumerate(head_urls):
        article = get_content(url)
        title = article[0]
        content = article[1]
        summary = summery_article(content)
        Headline.objects.create(
            url=url,
            title=title,
            summery=summary,
        )


# step3.실행 주기 설정
schedule.every().day.at("11:00:00").do(headline_summary)  # 매일 오전 11시에 실행
# schedule.every(1).minutes.do(headline_summary)


# step4.스캐쥴 시작
while True:
    schedule.run_pending()
    time.sleep(1)