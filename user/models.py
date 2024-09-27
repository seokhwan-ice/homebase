from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    nickname = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=10)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="user/image/%Y/%m/%d/", null=True, blank=True
    )
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        unique=True,
        validators=[RegexValidator(r"010-?[1-9]\d{3}-\d{4}")],
    )
    created_at = models.DateTimeField(auto_now_add=True)
