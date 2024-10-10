from openai import OpenAI
from homebase import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

system_instructions = """
너는 지금부터 야구 챗봇이야. 
사용자가 물어보는 질문에 대한 답과 함께
KBO 홈페이지의 링크를 제공하거나 스포츠 관련 기사의 url도 함께 가져와줘.
"""

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": "kbo 리그에는 어떤 팀이 있어?"},
    ],
)

print(completion.choices[0].message.content)