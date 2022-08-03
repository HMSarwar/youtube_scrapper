from celery import shared_task
from .views import sync_uploaded_videos as sync_video, sync_video_performance as sync_performance

@shared_task
def sync_uploaded_videos(*args, **kwargs):
    sync_video(*args, **kwargs)


@shared_task
def sync_video_performance(*args, **kwargs):
    sync_performance(*args, **kwargs)