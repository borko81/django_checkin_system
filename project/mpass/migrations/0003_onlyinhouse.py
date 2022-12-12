# Generated by Django 4.1.3 on 2022-12-12 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mpass", "0002_alter_personinformationmodel_group"),
    ]

    operations = [
        migrations.CreateModel(
            name="OnlyInHouse",
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
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mpass.cardsmodel",
                    ),
                ),
            ],
        ),
    ]