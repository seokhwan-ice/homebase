from django.db import models
from django.conf import settings


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Free(TimeStamp):
    title = models.CharField(max_length=25)
    content = models.TextField()
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    free_image = models.ImageField(
        upload_to="free/image/%Y/%m/%d/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]


class Live(TimeStamp):
    title = models.CharField(max_length=20)
    content = models.TextField()
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    live_image = models.ImageField(
        upload_to="live/image/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    game_date = models.DateTimeField()
    seat = models.CharField(max_length=20)
    team = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]
