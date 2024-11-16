from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management.settings')

app = Celery('library_management')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate_most_borrowed_books_report': {
        'task': 'reports.tasks.generate_most_borrowed_books_report',
        'schedule': crontab(hour=0, minute=0),  # روزانه در نیمه‌شب
    },
    'generate_overdue_borrowers_report': {
        'task': 'reports.tasks.generate_overdue_borrowers_report',
        'schedule': crontab(hour=0, minute=0),
    },
    'generate_checked_out_books_report': {
        'task': 'reports.tasks.generate_checked_out_books_report',
        'schedule': crontab(hour=0, minute=0),
    },
}