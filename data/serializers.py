from rest_framework import serializers
from data.models import GameRecord


class GameRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRecord
        fields = "__all__"  # 모든 필드를 포함
