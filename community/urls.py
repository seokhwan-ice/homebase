from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"free", views.FreeViewSet, basename="free")
router.register(r"live", views.LiveViewSet, basename="live")

urlpatterns = [
    path("", include(router.urls)),
]

# 자유게시판
# api/community/free/
# GET: 목록 / POST: 생성
# api/community/free/<pk>/
# GET: 상제 / PUT: 수정 / DELETE: 삭제
#
# 직관인증글
# api/community/live/
# GET: 목록 / POST: 생성
# api/community/live/<pk>/
# GET: 상제 / PUT: 수정 / DELETE: 삭제
