from django.db import models


class Headline(models.Model):
    url = models.URLField()
    title = models.TextField()
    summery = models.TextField()

    def __str__(self):
        return self.title
