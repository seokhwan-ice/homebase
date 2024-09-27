from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"free", views.FreeViewSet, basename="free")
router.register(r"live", views.LiveViewSet, basename="live")

urlpatterns = [
    path("", include(router.urls)),
]
