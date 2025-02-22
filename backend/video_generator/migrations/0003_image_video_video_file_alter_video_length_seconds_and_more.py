# Generated by Django 5.1.1 on 2024-10-02 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("video_generator", "0002_video_length_seconds_video_orientation_video_topic"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                ("prompt", models.TextField()),
                ("image_url", models.URLField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name="video",
            name="video_file",
            field=models.FileField(blank=True, null=True, upload_to="videos/"),
        ),
        migrations.AlterField(
            model_name="video",
            name="length_seconds",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="video",
            name="orientation",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="video",
            name="topic",
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name="video",
            name="images",
            field=models.ManyToManyField(to="video_generator.image"),
        ),
    ]
