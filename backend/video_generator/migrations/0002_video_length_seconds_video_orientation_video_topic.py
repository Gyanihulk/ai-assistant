# Generated by Django 5.1.1 on 2024-10-02 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("video_generator", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="length_seconds",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="video",
            name="orientation",
            field=models.CharField(
                choices=[("landscape", "Landscape"), ("portrait", "Portrait")],
                default="landscape",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="video",
            name="topic",
            field=models.CharField(default="General", max_length=200),
            preserve_default=False,
        ),
    ]
