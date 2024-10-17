from rest_framework import serializers
from .models import (
    PlayerRecord,
    GameRecord,
    TeamRank,
    Players,
    SportsNews,
    TeamRecord,
    TeamDetail,
)


class SportsNewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportsNews
        fields = "__all__"  # 모든 필드를 포함


class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = "__all__"  # 모든 필드를 포함


# 선수 기록 시리얼라이저
class PlayerRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerRecord
        fields = "__all__"  # 모든 필드를 포함


# 경기 기록 시리얼라이저
class GameRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRecord
        fields = [
            "date",
            "team_1",
            "team_2",
            "inning_scores_team_1",
            "inning_scores_team_2",
            "r_h_e_b_team_1",
            "r_h_e_b_team_2",
        ]


# 팀 순위 시리얼라이저
class TeamRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRank
        fields = [
            "rank",
            "team_name",
            "games_played",
            "wins",
            "draws",
            "losses",
            "games_behind",
            "win_rate",
            "streak",
            "last_10_games",
        ]


class TeamRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRecord
        fields = [
            "id",
            "team_name",
            "rival",
            "team_number",
            "wins",
            "draws",
            "losses",
            "win_rate",
        ]


class TeamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamDetail
        fields = "__all__"


class TeamRankGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRank
        fields = "__all__"  # 모든 필드 포함


# 팀 상대전적 시리얼라이저
class TeamRecordGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRecord
        fields = "__all__"  # 모든 필드 포함


# 팀 상세기록 시리얼라이저
class TeamDetailGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamDetail
        fields = "__all__"  # 모든 필드 포함
