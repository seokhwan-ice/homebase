from django.db import models


class PlayerRecord(models.Model):
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
        return self.name
