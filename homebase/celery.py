from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django의 설정 모듈을 Celery에서 사용할 수 있도록 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homebase.settings")

app = Celery("homebase")

# 여기서 Django의 설정을 Celery의 설정으로 덮어씁니다.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Django에서 자동으로 등록된 모든 task 모듈을 Celery에서 찾도록 설정합니다.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
