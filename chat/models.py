from django.db import models
from django.conf import settings


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# 채팅방
class ChatRoom(TimeStamp):
    title = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="chat/image/%Y/%m/%d/", null=True, blank=True)
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]


# 채팅 메시지
class ChatMessage(TimeStamp):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    def __str__(self):
        return f"{self.content[:10]} by {self.user}"


# 채팅방 참여자
class ChatParticipant(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE,
        related_name="participants",
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    # left_at = models.DateTimeField(null=True, blank=True)  # 안나갔으면 null 로 저장

    def __str__(self):
        return f"{self.user} in {self.room.title}"
