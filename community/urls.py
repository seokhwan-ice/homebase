from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"free", views.FreeViewSet, basename="free")

urlpatterns = [
    path("", include(router.urls)),
]


# api/community/free/
# GET: 목록 / POST: 생성

# api/community/free/<pk>/
# GET: 상제 / PUT: 수정 / DELETE: 삭제
