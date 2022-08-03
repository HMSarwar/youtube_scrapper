# Generated by Django 4.0.6 on 2022-08-01 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('videoId', models.CharField(max_length=512)),
                ('channelID', models.CharField(max_length=512)),
                ('total_view_count', models.IntegerField(default=0)),
                ('total_likes', models.IntegerField(default=0)),
                ('total_dislikes', models.IntegerField(default=0)),
                ('next_sync', models.DateTimeField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='VideoPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoId', models.CharField(max_length=512)),
                ('total_view_count', models.IntegerField(default=0)),
                ('total_likes', models.IntegerField(default=0)),
                ('total_dislikes', models.IntegerField(default=0)),
                ('timeframe', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VideoTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=512)),
                ('videoID', models.CharField(max_length=512)),
            ],
        ),
    ]