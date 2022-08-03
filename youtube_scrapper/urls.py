from django.urls import path
from .views import get_video_performance_data

urlpatterns = [
    path('', get_video_performance_data),
]
