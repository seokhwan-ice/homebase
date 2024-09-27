from rest_framework import serializers
from .models import UrlContent, Headline



class CrawlingSerializer(serializers.Serializer):
    url = serializers.URLField()
    title = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data):
        return UrlContent(**validated_data)


class HeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headline
        fields = ['url', 'title', 'summery']