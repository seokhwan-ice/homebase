from pathlib import Path
from selenium import webdriver
from selenium.wepipbdriver.chrome.service import Service
from bs4 import BeautifulSoup
from data.models import Headline
from django.db import IntegrityError

# 크롬 드라이버 경로 설정
base_dir = Path(__file__).resolve().parent
driver_path = base_dir / "chromedriver.exe"

def get_headlines():
    url = "https://mydaily.co.kr/baseball/general"

    # 크롬 드라이버 옵션 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--lang=ko_KR")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    )

    # 크롬 드라이버 실행
    service = Service(executable_path=str(driver_path))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(10)

    # 페이지 소스를 BeautifulSoup으로 파싱
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # 헤드라인 리스트 추출
    headline_list = soup.select("ul#section_list > li")

    if not headline_list:
        print("헤드라인이 없습니다. HTML 구조를 확인하세요.")
        driver.quit()
        return

    for headline in headline_list:
        # 제목 추출
        title_element = headline.select_one("div.title a")
        title = title_element.get_text(strip=True) if title_element else "No title found"

        # 요약 추출
        summary_element = headline.select_one("p.body a")
        summary = summary_element.get_text(strip=True) if summary_element else "No summary found"

        # 데이터베이스에 저장
        if not Headline.objects.filter(title=title).exists():
            try:
                Headline.objects.create(
                    url=url,
                    title=title,
                    summary=summary,
                )
                print(f"Saved headline: {title}")
            except IntegrityError:
                print(f"Headline already exists: {title}")

    driver.quit()