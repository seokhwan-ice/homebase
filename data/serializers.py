from rest_framework import serializers
from .models import UrlContent



class CrawlingSerializer(serializers.Serializer):
    url = serializers.URLField()
    title = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data):
        return UrlContent(**validated_data)

