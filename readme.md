Configure the local settings file to configure Database and Channel List txt file where the channels will be read from


Use Celery for background process to sync videos against the channel lists and also video performance

sample Celery Command:

```
celery beat -S redbeat.RedBeatScheduler -A scrapper_app --loglevel=INFO -b redis://localhost:6379/12
celery worker -S redbeat.RedBeatScheduler -A scrapper_app --loglevel=INFO -Q scrapper -b redis://localhost:6379/12
```

API URL:
```
/scrapper/api/video_list/
Expected Query params:
tags -- comma separated tag to get tag wise data
video_performance --  True/ False for getting data by video performance
channel_id -- for getting data of specific channel
```
