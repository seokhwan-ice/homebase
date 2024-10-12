# data/models.py
from django.db import models

class Players(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    batter_hand = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)  # 날짜 필드
    school = models.CharField(max_length=100, null=True, blank=True)
    draft_info = models.CharField(max_length=100, null=True, blank=True)
    active_years = models.CharField(max_length=50, null=True, blank=True)
    active_team = models.CharField(max_length=50, null=True, blank=True)
    profile_img = models.URLField(null=True, blank=True)  # 이미지 URL 필드

    def __str__(self):
        return self.name

