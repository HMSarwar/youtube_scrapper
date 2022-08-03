from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=512)
    videoId = models.CharField(max_length=512)
    channelID = models.CharField(max_length=512)
    published_at = models.DateTimeField(default=None)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    next_sync = models.DateTimeField(default=None)


class VideoPerformance(models.Model):
    videoId = models.CharField(max_length=512)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    timeframe = models.IntegerField(default=0)


class VideoTags(models.Model):
    tag = models.CharField(max_length=512)
    videoID = models.CharField(max_length=512)


class ChannelWiseLastSync(models.Model):
    channelID = models.CharField(max_length=512, )
    last_sync = models.DateTimeField(default=None)

