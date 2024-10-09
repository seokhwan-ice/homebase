from email.policy import default

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
        related_name="author_free",
    )
    free_image = models.ImageField(
        upload_to="free/image/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    views = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Free[{self.id}]{self.title}"

    def update_comments_count(self):
        self.comments_count = Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).count()
        self.save()

    class Meta:
        ordering = ["-id"]


class Live(TimeStamp):
    TEAM_CHOICES = [
        ("LG 트윈스", "LG 트윈스"),
        ("KT 위즈", "KT 위즈"),
        ("SSG 랜더스", "SSG 랜더스"),
        ("NC 다이노스", "NC 다이노스"),
        ("두산 베어스", "두산 베어스"),
        ("KIA 타이거즈", "KIA 타이거즈"),
        ("롯데 자이언츠", "롯데 자이언츠"),
        ("삼성 라이온즈", "삼성 라이온즈"),
        ("한화 이글스", "한화 이글스"),
        ("키움 히어로즈", "키움 히어로즈"),
    ]
    STADIUM_CHOICES = [
        ("잠실", "잠실 야구장"),
        ("수원", "수원 KT 위즈파크"),
        ("문학", "인천 SSG 랜더스필드"),
        ("창원", "창원 NC 파크"),
        ("광주", "광주 기아 챔피언스필드"),
        ("사직", "사직 야구장"),
        ("대구", "대구 삼성 라이온즈파크"),
        ("대전", "대전 한밭 야구장"),
        ("고척", "고척 스카이돔"),
    ]
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_live",
    )
    live_image = models.ImageField(
        upload_to="live/image/%Y/%m/%d/",
        blank=True,
        null=True,
    )  # TODO: 이미지 필수 + 영상필드추가/seat,team필드수정

    review = models.TextField()
    game_date = models.DateTimeField()
    home_team = models.CharField(max_length=20, choices=TEAM_CHOICES)
    away_team = models.CharField(max_length=20, choices=TEAM_CHOICES)
    stadium = models.CharField(max_length=20, choices=STADIUM_CHOICES)
    seat = models.CharField(max_length=20, blank=True, null=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Live[{self.id}]"

    def update_likes_count(self):
        self.likes_count = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).count()
        self.save()

    def update_comments_count(self):
        self.comments_count = Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).count()
        self.save()

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
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Comment[{self.id}] - by:{self.author} on:{self.content_object}"

    def update_likes_count(self):
        self.likes_count = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        ).count()
        self.save()

    class Meta:
        ordering = ["-id"]


class Like(TimeStamp):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Like - by:{self.user} on:{self.content_object}"

    class Meta:  # 한 유저는 같은 글에 한번만 좋아요 가능
        unique_together = ("user", "content_type", "object_id")


class Bookmark(TimeStamp):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Bookmark - by:{self.user} on:{self.content_object}"

    class Meta:  # 한 유저는 같은 글에 한번만 북마크 가능
        unique_together = ("user", "content_type", "object_id")
