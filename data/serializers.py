from rest_framework import serializers
from .models import PlayerRecord, GameRecord, TeamRank, Players


class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = "__all__"  # 모든 필드를 포함


# 선수 기록 시리얼라이저
class PlayerRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerRecord
        fields = [
            "team_logo_url",
            "name",
            "opponent",
            "pa",
            "epa",
            "ab",
            "r",
            "h",
            "two_b",
            "three_b",
            "hr",
            "tb",
            "rbi",
            "bb",
            "hp",
            "ib",
            "so",
            "gdp",
            "sh",
            "sf",
            "avg",
            "obp",
            "slg",
            "ops",
            "np",
            "avli",
            "re24",
            "wpa",
        ]


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
