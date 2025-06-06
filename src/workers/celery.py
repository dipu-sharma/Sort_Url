from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "workers",
    broker="redis://localhost:6379/0",
    backend="rpc://"
)

celery_app.conf.beat_schedule = {
    'delete-expire-urls': {
        'task': 'src.api.tasks.expire_urls',
        'schedule': crontab(hour=0, minute=0), 
    },
}
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=3600,
    broker_connection_retry_on_startup = True
)