from django.urls import path
from . import views

app_name = "data"
urlpatterns = [
    path("sports_news/", views.SportsNewsAPIView.as_view(), name='sports_news'),
]
