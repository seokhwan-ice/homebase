# Generated by Django 4.2 on 2024-10-08 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChatRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=20, unique=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="chat/image/%Y/%m/%d/"
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
    ]
