# Generated by Django 5.1.1 on 2024-10-02 06:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "video_generator",
            "0003_image_video_video_file_alter_video_length_seconds_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="video",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="image_videos",
                to="video_generator.video",
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="image_url",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="video",
            name="images",
            field=models.ManyToManyField(
                related_name="videos", to="video_generator.image"
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="orientation",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="video",
            name="published_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
