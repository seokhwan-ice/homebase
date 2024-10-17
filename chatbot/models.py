from django.db import models

class Conversation(models.Model): 
    user_input = models.TextField()  # 사용자의 입력
    ai_response = models.TextField()  # AI의 응답
    timestamp = models.DateTimeField(auto_now_add=True)  # 대화가 이루어진 시간

    def __str__(self):
        return f"{self.user_input[:50]} - {self.ai_response[:50]}"
