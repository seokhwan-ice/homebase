from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from .models import ChatResponse

class ChatbotView(View):
    def post(self, request):
        user_input = request.POST.get('message')
        
        # 데이터베이스에서 응답 가져오기
        response = ChatResponse.objects.filter(user_input=user_input).first()
        
        if response:
            return JsonResponse({"response": response.response})
        else:
            return JsonResponse({"response": "죄송합니다, 이해하지 못했습니다."})
