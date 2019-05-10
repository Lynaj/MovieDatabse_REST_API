from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('cryptojobber')

app.config_from_object('django.conf:settings')

app = Celery()

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from apps.misc.tasks import update_ethereum_price_task

    sender.add_periodic_task(12.0, update_ethereum_price_task.s(),
                             name='update_ethereum_price_task')

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
