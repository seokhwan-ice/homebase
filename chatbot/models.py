from django.db import models

class ChatResponse(models.Model):
    user_input = models.CharField(max_length=255)
    response = models.TextField()

    def __str__(self):
        return self.user_input

