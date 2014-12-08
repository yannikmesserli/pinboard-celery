# config file for Celery Daemon

# default RabbitMQ broker
BROKER_URL = 'amqp://'

# default RabbitMQ backend
CELERY_RESULT_BACKEND = 'amqp://'


from celery.schedules import crontab

CELERY_TIMEZONE = 'Europe/Zurich'

CELERYBEAT_SCHEDULE = {
    # Executes every Day morning at 8:00 A.M, except Sunday (no work Sunday!)
    'add-every-morning': {
        'task': 'framework.tasks.fetch_pinboard',
        'schedule': crontab(hour=8, minute=0, day_of_week=[0,1,2,3,4,5])
    },
}