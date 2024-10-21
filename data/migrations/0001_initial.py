# Generated by Django 4.2 on 2024-10-21 03:50

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
                ("player_number", models.IntegerField()),
                ("name", models.CharField(max_length=100)),
                ("team_name", models.CharField(max_length=50)),
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
            name="SportsNews",
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
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(blank=True, max_length=100, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("url", models.URLField()),
                ("published_at", models.DateTimeField()),
                ("content", models.TextField(blank=True, null=True)),
                ("image_url", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="TeamDetail",
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
                ("team_number", models.CharField(max_length=10)),
                ("team", models.CharField(max_length=100)),
                ("year", models.FloatField()),
                ("war", models.FloatField()),
                ("owar", models.FloatField()),
                ("dwar", models.FloatField()),
                ("games", models.FloatField()),
                ("plate_appearances", models.FloatField()),
                ("effective_pa", models.FloatField()),
                ("at_bats", models.FloatField()),
                ("runs", models.FloatField()),
                ("hits", models.FloatField()),
                ("two_b", models.FloatField()),
                ("three_b", models.FloatField()),
                ("home_runs", models.FloatField()),
                ("total_bases", models.FloatField()),
                ("rbi", models.FloatField()),
                ("stolen_bases", models.FloatField()),
                ("caught_stealing", models.FloatField()),
                ("walks", models.FloatField()),
                ("hit_by_pitch", models.FloatField()),
                ("intentional_walks", models.FloatField()),
                ("strikeouts", models.FloatField()),
                ("grounded_into_double_play", models.FloatField()),
                ("sacrifice_hits", models.FloatField()),
                ("sacrifice_flies", models.FloatField()),
                ("batting_average", models.FloatField()),
                ("on_base_percentage", models.FloatField()),
                ("slugging_percentage", models.FloatField()),
                ("on_base_plus_slugging", models.FloatField()),
                ("runs_per_effective_pa", models.FloatField()),
                ("wrc_plus", models.FloatField()),
            ],
            options={
                "verbose_name": "팀 통계",
                "verbose_name_plural": "팀 통계",
            },
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
                ("team_number", models.CharField(max_length=10)),
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
            name="TeamRecord",
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
                ("team_name", models.CharField(max_length=50)),
                ("team_number", models.CharField(max_length=10)),
                ("rival", models.CharField(max_length=50)),
                ("wins", models.IntegerField()),
                ("draws", models.IntegerField()),
                ("losses", models.IntegerField()),
                ("win_rate", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Video",
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
                ("video_id", models.CharField(max_length=100, unique=True)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("publish_time", models.DateTimeField()),
                ("video_url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="WeatherData",
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
                ("base_date", models.CharField(max_length=8)),
                ("base_time", models.CharField(max_length=4)),
                ("location", models.CharField(max_length=50)),
                ("temperature", models.FloatField()),
                ("humidity", models.FloatField()),
                ("wind_speed", models.FloatField()),
                ("wind_direction", models.CharField(max_length=10)),
                ("rain_status", models.CharField(max_length=10)),
                ("rain_probability", models.FloatField(blank=True, null=True)),
                ("sky_status", models.CharField(blank=True, max_length=10, null=True)),
                ("precipitation", models.FloatField(blank=True, null=True)),
                ("min_temperature", models.FloatField(blank=True, null=True)),
                ("max_temperature", models.FloatField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
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
                ("player_number", models.IntegerField()),
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
                ("url", models.URLField()),
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
