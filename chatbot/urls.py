from django.urls import path
from .views import get_player_info

urlpatterns = [
    path('get-player-info/', get_player_info, name='get_player_info'),
]
