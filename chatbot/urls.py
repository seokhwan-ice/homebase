from django.urls import path
from chatbot.views import ChatResponseView

urlpatterns = [
    path('get-response/', ChatResponseView.as_view(), name='get_chat_response'),
]
