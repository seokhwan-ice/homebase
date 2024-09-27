import openai
from django.contrib.sites import requests  # <- 수정된 부분
from homebase.config import OPENAI_API_KEY
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .crawling import get_content
from .models import UrlContent, Headline
from .serializers import CrawlingSerializer

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


class TodayHeadlineAPIView(APIView):
    def get(self, request):
        headline_articles = Headline.objects.all().order_by("-id")[:5]
        serializer = CrawlingSerializer(headline_articles, many=True)
        return Response(serializer.data)
