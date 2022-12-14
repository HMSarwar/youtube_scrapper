# Generated by Django 4.0.6 on 2022-08-02 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_scrapper', '0003_video_published_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='total_dislikes',
            new_name='comment_count',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='total_likes',
            new_name='favorite_count',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='total_view_count',
            new_name='like_count',
        ),
        migrations.RenameField(
            model_name='videoperformance',
            old_name='total_dislikes',
            new_name='comment_count',
        ),
        migrations.RenameField(
            model_name='videoperformance',
            old_name='total_likes',
            new_name='favorite_count',
        ),
        migrations.RenameField(
            model_name='videoperformance',
            old_name='total_view_count',
            new_name='like_count',
        ),
        migrations.AddField(
            model_name='video',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='videoperformance',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
