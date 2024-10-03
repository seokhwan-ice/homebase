from django.urls import path
from . import views

urlpatterns = [
    path(
        "chatrooms/",
        views.ChatRoomListCreateView.as_view(),
        name="chatroom_list_create",
    ),
    path(
        "chatrooms/<int:id>/",
        views.ChatRoomDetailView.as_view(),
        name="chatroom_detail",
    ),
    path("", views.test_page1, name="test_page1"),
    path("<str:room_name>/", views.test_page2, name="test_page2"),
]
