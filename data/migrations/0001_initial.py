# Generated by Django 4.2 on 2024-10-10 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Players",
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
                ("name", models.CharField(max_length=100)),
                ("team", models.CharField(max_length=50)),
                ("position", models.CharField(max_length=50)),
                ("batter_hand", models.CharField(max_length=10)),
                ("birth_date", models.DateField(blank=True, null=True)),
                ("school", models.CharField(blank=True, max_length=100, null=True)),
                ("draft_info", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "active_years",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("active_team", models.CharField(blank=True, max_length=50, null=True)),
                ("profile_img", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="TeamRank",
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
                ("games_played", models.IntegerField()),
                ("wins", models.IntegerField()),
                ("draws", models.IntegerField()),
                ("losses", models.IntegerField()),
                ("games_behind", models.FloatField()),
                ("win_rate", models.FloatField()),
                ("streak", models.CharField(max_length=10)),
                ("last_10_games", models.CharField(max_length=20)),
            ],
            options={
                "verbose_name": "Team Record",
                "verbose_name_plural": "Team Records",
                "db_table": "data_teamrank",
                "ordering": ["rank"],
            },
        ),
        migrations.CreateModel(
            name="PlayerRecord",
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
                ("team_logo_url", models.URLField(max_length=255)),
                ("name", models.CharField(max_length=100)),
                ("opponent", models.CharField(max_length=100)),
                ("pa", models.IntegerField(default=0)),
                ("epa", models.IntegerField(default=0)),
                ("ab", models.IntegerField(default=0)),
                ("r", models.IntegerField(default=0)),
                ("h", models.IntegerField(default=0)),
                ("two_b", models.IntegerField(default=0)),
                ("three_b", models.IntegerField(default=0)),
                ("hr", models.IntegerField(default=0)),
                ("tb", models.IntegerField(default=0)),
                ("rbi", models.IntegerField(default=0)),
                ("bb", models.IntegerField(default=0)),
                ("hp", models.IntegerField(default=0)),
                ("ib", models.IntegerField(default=0)),
                ("so", models.IntegerField(default=0)),
                ("gdp", models.IntegerField(default=0)),
                ("sh", models.IntegerField(default=0)),
                ("sf", models.IntegerField(default=0)),
                ("avg", models.FloatField(default=0.0)),
                ("obp", models.FloatField(default=0.0)),
                ("slg", models.FloatField(default=0.0)),
                ("ops", models.FloatField(default=0.0)),
                ("np", models.IntegerField(default=0)),
                ("avli", models.FloatField(default=0.0)),
                ("re24", models.FloatField(default=0.0)),
                ("wpa", models.FloatField(default=0.0)),
            ],
            options={
                "unique_together": {("name", "opponent")},
            },
        ),
        migrations.CreateModel(
            name="GameRecord",
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
                ("date", models.DateField()),
                ("team_1", models.CharField(max_length=100)),
                ("team_2", models.CharField(max_length=100)),
                ("inning_scores_team_1", models.JSONField(default=list)),
                ("inning_scores_team_2", models.JSONField(default=list)),
                ("r_h_e_b_team_1", models.JSONField(blank=True, default=dict)),
                ("r_h_e_b_team_2", models.JSONField(blank=True, default=dict)),
            ],
            options={
                "db_table": "data_gamerecord",
                "unique_together": {("date", "team_1", "team_2")},
            },
        ),
    ]
