# Generated by Django 4.2 on 2024-10-18 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bookmark",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("content", models.TextField()),
                ("object_id", models.PositiveIntegerField()),
                ("likes_count", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Free",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=30)),
                ("content", models.TextField()),
                (
                    "free_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="free/image/%Y/%m/%d/"
                    ),
                ),
                ("views", models.PositiveIntegerField(default=0)),
                ("comments_count", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Like",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Live",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "live_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="live/image/%Y/%m/%d/"
                    ),
                ),
                ("review", models.TextField()),
                ("game_date", models.DateTimeField()),
                (
                    "home_team",
                    models.CharField(
                        choices=[
                            ("LG 트윈스", "LG 트윈스"),
                            ("KT 위즈", "KT 위즈"),
                            ("SSG 랜더스", "SSG 랜더스"),
                            ("NC 다이노스", "NC 다이노스"),
                            ("두산 베어스", "두산 베어스"),
                            ("KIA 타이거즈", "KIA 타이거즈"),
                            ("롯데 자이언츠", "롯데 자이언츠"),
                            ("삼성 라이온즈", "삼성 라이온즈"),
                            ("한화 이글스", "한화 이글스"),
                            ("키움 히어로즈", "키움 히어로즈"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "away_team",
                    models.CharField(
                        choices=[
                            ("LG 트윈스", "LG 트윈스"),
                            ("KT 위즈", "KT 위즈"),
                            ("SSG 랜더스", "SSG 랜더스"),
                            ("NC 다이노스", "NC 다이노스"),
                            ("두산 베어스", "두산 베어스"),
                            ("KIA 타이거즈", "KIA 타이거즈"),
                            ("롯데 자이언츠", "롯데 자이언츠"),
                            ("삼성 라이온즈", "삼성 라이온즈"),
                            ("한화 이글스", "한화 이글스"),
                            ("키움 히어로즈", "키움 히어로즈"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "stadium",
                    models.CharField(
                        choices=[
                            ("잠실", "잠실 야구장"),
                            ("수원", "수원 KT 위즈파크"),
                            ("문학", "인천 SSG 랜더스필드"),
                            ("창원", "창원 NC 파크"),
                            ("광주", "광주 기아 챔피언스필드"),
                            ("사직", "사직 야구장"),
                            ("대구", "대구 삼성 라이온즈파크"),
                            ("대전", "대전 한밭 야구장"),
                            ("고척", "고척 스카이돔"),
                        ],
                        max_length=20,
                    ),
                ),
                ("seat", models.CharField(blank=True, max_length=20, null=True)),
                ("likes_count", models.PositiveIntegerField(default=0)),
                ("comments_count", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
    ]
