# Generated by Django 4.2 on 2024-10-13 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="playerrecord",
            name="team_logo_url",
        ),
    ]