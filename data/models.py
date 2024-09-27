from django.db import models


class UrlContent(models.Model):
    url = models.URLField(unique=True)  # URL 필드
    title = models.CharField(max_length=255)  # 제목 필드
    content = models.TextField()  # 기사 내용 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일 자동 추가

    def __str__(self):
        return self.title


class Headline(models.Model):
    url = models.URLField()
    title = models.TextField()
    summery = models.TextField()

    def __str__(self):
        return self.title
