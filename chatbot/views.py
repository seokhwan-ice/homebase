from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatbot.models import ChatResponse
from rest_framework.permissions import AllowAny

class ChatResponseView(APIView):
    permission_classes = [AllowAny]  # 필요한 권한 설정

    def post(self, request):
        user_input = request.data.get('user_input')

        if user_input is None:
            return Response({'error': 'user_input is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 입력된 user_input과 일치하는 답변 검색
            response = ChatResponse.objects.get(user_input=user_input).response
        except ChatResponse.DoesNotExist:
            # 일치하는 데이터가 없을 경우 기본 응답 설정
            response = "죄송합니다, 해당 질문에 대한 답변이 없습니다."

        return Response({'response': response}, status=status.HTTP_200_OK)
