import openai
import requests
from homebase.config import OPENAI_API_KEY
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .crawling import get_content
from .models import UrlContent, Headline
from .serializers import CrawlingSerializer, HeadlineSerializer
from bs4 import BeautifulSoup

openai.api_key = OPENAI_API_KEY


class CrawlingAPIView(APIView):
    def post(self, request):
        url = request.data.get("url")

        if not url:
            return Response("URL이 제공되지 않았습니다.", status=status.HTTP_400_BAD_REQUEST)

        try:
            # 세션 생성
            session = requests.Session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
            }
            session.headers.update(headers)

            web_site = session.get(url)

            if web_site.status_code != 200:
                return Response(f"찾을 수 없는 URL입니다. 상태 코드: {web_site.status_code}", status=status.HTTP_400_BAD_REQUEST)

            # 콘텐츠 가져오기
            crawling = get_content(url)
            title = crawling[0]
            content = crawling[1]

            # 데이터베이스에 이미 있는 URL이라면 저장하지 않기
            if not UrlContent.objects.filter(url=url).exists():
                UrlContent.objects.create(
                    url=url,
                    title=title,
                    content=content,
                )

            serializer = CrawlingSerializer(data={"url": url, "title": title, "content":content})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response(f"요청 오류: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HeadlineAPIView(APIView):
    def fetch_titles_from_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch content from {url}, status code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')
        title_tags = soup.find_all('p', class_='title')  # 모든 기사 제목을 찾는 로직
        titles = []

        for title_tag in title_tags:
            title = title_tag.get_text(strip=True)  # 텍스트 가져오기
            if title:
                titles.append(title)
            else:
                titles.append("제목을 찾을 수 없습니다")

        return titles

    def get(self, request):
        url = 'https://www.mydaily.co.kr/baseball/general'

        try:
            titles = self.fetch_titles_from_url(url)
            return Response(titles, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def generate_summary(self, text):
        # OpenAI API를 사용해 요약
        OPENAI_API_KEY="sk-2aqHIQrXArx_d_Eu_TCY1DxlvxefpLOMWxO6RHDFOxT3BlbkFJtk8dniaOW8E5rprxgkaoPK_glBRmr9pvlUtYSPPYMA"
  # 올바른 API 키로 수정

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 최신 ChatGPT 모델 사용
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following text: {text}"}
            ],
            max_tokens=200,  # 요약된 텍스트 길이
            temperature=0.7  # creativity 옵션
        )
        summary = response.choices[0].message['content'].strip()
        return summary


'''
마무리글  크롤링을 하느데 리스트 크롤링을해야함...리스트들도 크롤링 해오고 리스트 안에 있는 자료들도 크롤링해야함
근데 안됨... 왜??? 뭐때문에???????? 로직 전체를 수정해야 할것 같음.

'''

