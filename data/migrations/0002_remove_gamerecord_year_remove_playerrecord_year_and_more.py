# Generated by Django 4.2 on 2024-10-21 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gamerecord",
            name="year",
        ),
        migrations.RemoveField(
            model_name="playerrecord",
            name="year",
        ),
        migrations.RemoveField(
            model_name="players",
            name="year",
        ),
        migrations.RemoveField(
            model_name="teamrank",
            name="year",
        ),
        migrations.RemoveField(
            model_name="teamrecord",
            name="year",
        ),
    ]