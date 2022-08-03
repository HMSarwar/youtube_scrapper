from django.apps import AppConfig


class Video(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video'

class VideoPerformance(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_performance'
