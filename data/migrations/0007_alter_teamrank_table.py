# Generated by Django 4.2 on 2024-10-08 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0006_rename_teamrecord_teamrank"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="teamrank",
            table="data_teamrank",
        ),
    ]
