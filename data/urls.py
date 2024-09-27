from django.urls import path
from . import views


urlpatterns = [
    path("crawling/", views.CrawlingAPIView.as_view()),
    path("headline/", views.TodayHeadlineAPIView.as_view()),
]
