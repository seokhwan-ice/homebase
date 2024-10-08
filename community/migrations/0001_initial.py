# Generated by Django 4.2 on 2024-10-01 08:39

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
                ("title", models.CharField(max_length=25)),
                ("content", models.TextField()),
                (
                    "free_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="free/image/%Y/%m/%d/"
                    ),
                ),
                ("views", models.PositiveIntegerField(default=0)),
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
                            ("lg_twins", "LG 트윈스"),
                            ("kt_wiz", "KT 위즈"),
                            ("ssg_landers", "SSG 랜더스"),
                            ("nc_dinos", "NC 다이노스"),
                            ("doosan_bears", "두산 베어스"),
                            ("kia_tigers", "KIA 타이거즈"),
                            ("lotte_giants", "롯데 자이언츠"),
                            ("samsung_lions", "삼성 라이온즈"),
                            ("hanwha_eagles", "한화 이글스"),
                            ("kiwoom_heroes", "키움 히어로즈"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "away_team",
                    models.CharField(
                        choices=[
                            ("lg_twins", "LG 트윈스"),
                            ("kt_wiz", "KT 위즈"),
                            ("ssg_landers", "SSG 랜더스"),
                            ("nc_dinos", "NC 다이노스"),
                            ("doosan_bears", "두산 베어스"),
                            ("kia_tigers", "KIA 타이거즈"),
                            ("lotte_giants", "롯데 자이언츠"),
                            ("samsung_lions", "삼성 라이온즈"),
                            ("hanwha_eagles", "한화 이글스"),
                            ("kiwoom_heroes", "키움 히어로즈"),
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
            ],
            options={
                "ordering": ["-id"],
            },
        ),
    ]