# Generated by Django 4.2 on 2024-10-20 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatroom",
            name="description",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
