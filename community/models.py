from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
        related_name="free_title",

    )
    free_image = models.ImageField(
        upload_to="free/image/%Y/%m/%d/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Free[{self.id}]{self.title}"

    class Meta:
        ordering = ["-id"]


class Live(TimeStamp):
    title = models.CharField(max_length=20)
    content = models.TextField()
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_live"
    )
    live_image = models.ImageField(
        upload_to="live/image/%Y/%m/%d/",
        blank=True,
        null=True,
    )  # TODO: 이미지 필수여부 논의 + 영상필드추가/seat,team필드수정
    game_date = models.DateTimeField()
    seat = models.CharField(max_length=20)
    team = models.CharField(max_length=20)

    def __str__(self):
        return f"Live[{self.id}]{self.title}"

    class Meta:
        ordering = ["-id"]


class Comment(TimeStamp):  # TODO: 데이터베이스 인덱스 추가 / 대.댓글 성능최적화
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    # 여러 모델(Free,Live,+a)에 ForeignKey
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    # 대댓글
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Comment[{self.id}] - by:{self.author} on:{self.content_object}"

    class Meta:
        ordering = ["-id"]
