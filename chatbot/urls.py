# urls.py

from django.urls import path
from .views import ConversationAPIView

urlpatterns = [
    path('api/conversations/', ConversationAPIView.as_view(), name='conversation-list-create'),
]
