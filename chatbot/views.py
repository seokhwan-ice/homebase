import openai
from homebase import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation
from .serializers import ConversationSerializer
from data.models import Players, PlayerRecord, GameRecord, TeamRank


def get_openai_response(user_input):
    openai.api_key = config.OPENAI_API_KEY
    prompt = f"사용자: {user_input}\nAI:"

    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=["사용자:", "AI:"],
    )

    return response.choices[0].text.strip()

# 대화 기록 저장 및 조회 API
class ConversationAPIView(APIView):

    # GET 요청: 대화 기록 조회
    def get(self, request, *args, **kwargs):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)  # POST 요청: 대화 생성 및 저장
    def post(self, request, *args, **kwargs):
        user_input = request.data.get('user_input')
        if user_input:
            # OpenAI API를 통해 응답 생성
            ai_response = get_openai_response(user_input)

            # 대화 기록을 데이터베이스에 저장
            conversation = Conversation.objects.create(
                user_input=user_input,
                ai_response=ai_response
            )
            # 생성된 대화 기록을 직렬화하여 반환
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'user_input is required'}, status=status.HTTP_400_BAD_REQUEST)

