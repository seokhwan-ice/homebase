from django.urls import path
from .views import ChatbotAPIView

urlpatterns = [
    # 대화 기록 API
    path("conversations/", ChatbotAPIView.as_view(), name="conversations"),
]
