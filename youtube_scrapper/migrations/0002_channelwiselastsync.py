# Generated by Django 4.0.6 on 2022-08-01 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_scrapper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelWiseLastSync',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channelID', models.CharField(max_length=512)),
                ('last_sync', models.DateTimeField(default=None)),
            ],
        ),
    ]
