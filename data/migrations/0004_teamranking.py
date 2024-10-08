# Generated by Django 4.2 on 2024-10-07 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0003_remove_gamerecord_b_team_1_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TeamRanking",
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
                ("rank", models.IntegerField()),
                ("team_name", models.CharField(max_length=100)),
                ("logo_url", models.URLField()),
                ("games_played", models.IntegerField()),
                ("wins", models.IntegerField()),
                ("draws", models.IntegerField()),
                ("losses", models.IntegerField()),
                ("games_behind", models.DecimalField(decimal_places=1, max_digits=4)),
                ("win_rate", models.DecimalField(decimal_places=3, max_digits=4)),
                ("streak", models.CharField(max_length=10)),
                ("recent_10_games", models.CharField(max_length=20)),
            ],
        ),
    ]