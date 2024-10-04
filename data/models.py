from django.db import models


class PlayerRecord(models.Model):
    team_logo_url = models.URLField(max_length=255)
    name = models.CharField(max_length=100)
    opponent = models.CharField(max_length=100)
    pa = models.IntegerField(default=0)
    epa = models.IntegerField(default=0)
    ab = models.IntegerField(default=0)
    r = models.IntegerField(default=0)
    h = models.IntegerField(default=0)
    two_b = models.IntegerField(default=0)
    three_b = models.IntegerField(default=0)
    hr = models.IntegerField(default=0)
    tb = models.IntegerField(default=0)
    rbi = models.IntegerField(default=0)
    bb = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    ib = models.IntegerField(default=0)
    so = models.IntegerField(default=0)
    gdp = models.IntegerField(default=0)
    sh = models.IntegerField(default=0)
    sf = models.IntegerField(default=0)
    avg = models.FloatField(default=0.0)
    obp = models.FloatField(default=0.0)
    slg = models.FloatField(default=0.0)
    ops = models.FloatField(default=0.0)
    np = models.IntegerField(default=0)
    avli = models.FloatField(default=0.0)
    re24 = models.FloatField(default=0.0)
    wpa = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.team_logo_url} {self.name}"

    class Meta:
        unique_together = ("name", "opponent")  # name과 opponent 조합이 유니크해야 함


class GameRecord(models.Model):
    date = models.DateField()
    team_1 = models.CharField(max_length=100)
    team_2 = models.CharField(max_length=100)
    inning_scores_team_1 = models.JSONField(default=list)  # JSONField 사용
    inning_scores_team_2 = models.JSONField(default=list)
    r_h_e_b_team_1 = models.JSONField(
        blank=True, default=dict
    )  # 팀 1의 R, H, E, B 값 저장
    r_h_e_b_team_2 = models.JSONField(
        blank=True, default=dict
    )  # 팀 2의 R, H, E, B 값 저장

    class Meta:
        unique_together = (("date", "team_1", "team_2"),)
        db_table = "data_gamerecord"  # 테이블 이름을 명시적으로 설정

    def __str__(self):
        return f"{self.date}: {self.team_1} vs {self.team_2}"
