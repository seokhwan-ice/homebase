# Generated by Django 4.2 on 2024-10-21 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Conversation",
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
                ("user_input", models.TextField()),
                ("ai_response", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
