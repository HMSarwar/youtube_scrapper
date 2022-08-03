from __future__ import absolute_import, unicode_literals
import os
import sys
import site

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapper.settings')
SITE_ROOT = os.path.dirname(__file__)
sys.path.append(SITE_ROOT)

import warnings

from celery import Celery
from django.conf import settings
from scrapper.settings import redbeat_redis_url

# set the default Django settings module for the 'celery' program.

app = Celery('main_celery_app')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS_WITH_TASKS)

app.conf.task_reject_on_worker_lost = True
app.conf.task_acks_late = True
app.conf.task_always_eager = True
app.conf.broker_pool_limit = True
app.conf.redbeat_redis_url = redbeat_redis_url


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
