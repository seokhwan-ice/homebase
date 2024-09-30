import openai
from config import OPENAI_API_KEY  # 설정 파일에서 OpenAI API 키 가져오기

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY  # 키를 설정합니다

def summery_article(article):
    system_instructions = """ 기사의 내용을 요약해줬으면 해. 
    내용은 공백을 제외하고 400자 이내로 요약해줘.
    내가 입력하는 프롬프트에는 불필요한 내용도 포함하고 있을 수 있으니 잘 구분해서 요약해줘.
    """

    # GPT 모델 사용
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # 모델 이름 확인
        messages=[
            {
                "role": "system",
                "content": system_instructions,
            },
            {
                "role": "user",
                "content": article,
            },
        ],
        max_tokens=400,  # 400자로 제한
    )

    # 결과 반환
    return completion.choices[0].message['content']