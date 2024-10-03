from django.db import models
from django.conf import settings


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# 채팅방
class ChatRoom(TimeStamp):
    name = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to="chat/image/%Y/%m/%d/", null=True, blank=True)
    creator = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


# # 채팅 메시지
# class ChatMessage(TimeStamp):
#     message = models.TextField()
#     chatroom = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE)
#     user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#
# # 참여자
# class ChatParticipant(models.Model):
#     chatroom = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE)
#     user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     joined_at = models.DateTimeField(auto_now_add=True)
#     left_at = models.DateTimeField(null=True, blank=True)  # 안나갔으면 null 로 저장

