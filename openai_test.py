from openai import OpenAI
from homebase.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def summery_article(article):
    system_instructions = """ 기사의 내용을 요약해줬으면 해. 
    내용은 공백을 제외하고 400자 이내로 요약해줘.
    내가 입력하는 프롬프트에는 불필요한 내용도 포함하고 있을 수 있으니 잘 구분해서 요약해줘.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
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
        max_tokens=500,
    )
    return completion.choices[0].message.content