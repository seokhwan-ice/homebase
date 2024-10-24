from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"chatrooms", views.ChatRoomViewSet, basename="chatrooms")
router.register(r"messages", views.ChatMessageViewSet, basename="messages")

urlpatterns = [
    path("", include(router.urls)),
]
