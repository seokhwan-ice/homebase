from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def get_content(url):
    # 크롬 드라이버 옵션
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # 새 창 없는 모드
    chrome_options.add_argument("lang=ko_KR")  # 한국어
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3)  # 3초 대기

    # 웹 페이지의 HTML 소스 가져오기
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

    # 제목 추출
    title_element = soup.select_one("div.article_head h1.title")
    title = title_element.get_text(strip=True) if title_element else "No title found"

    # 기사 내용 추출
    content_element = soup.select_one("div.article_content")
    content = content_element.get_text(strip=True) if content_element else "No content found"

    # 드라이버 종료
    driver.quit()


    return title, content