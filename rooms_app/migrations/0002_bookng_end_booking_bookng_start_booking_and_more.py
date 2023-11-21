# Generated by Django 4.2.7 on 2023-11-19 13:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rooms_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookng",
            name="end_booking",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="bookng",
            name="start_booking",
            field=models.DateField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name="bookng",
            unique_together={("user", "room")},
        ),
    ]
