import openai
from .models import Headline
from homebase.config import OPENAI_API_KEY  # 설정 파일에서 OpenAI API 키 가져오기

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

def summarize_headlines():
    # 데이터베이스에서 최근 헤드라인 5개 가져오기
    recent_headlines = Headline.objects.all().order_by("-id")[:5]
    summaries = []

    for headline in recent_headlines:
        # OpenAI API를 이용한 요약 요청
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"뉴스 제목: {headline.title}\n뉴스 내용: {headline.summery}\n위 뉴스를 요약해 주세요:",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        summary = response.choices[0].text.strip()
        summaries.append({
            "title": headline.title,
            "summary": summary
        })

    return summaries

if __name__ == "__main__":
    summarized_headlines = summarize_headlines()
    for headline in summarized_headlines:
        print(f"Title: {headline['title']}")
        print(f"Summary: {headline['summary']}")
        print("-" * 40)