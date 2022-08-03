from django.test import TestCase

# Create your tests here.
from .views import sync_uploaded_videos as sync_video, sync_video_performance as sync_performance


if __name__ == '__main__':
    sync_video()
    sync_performance()