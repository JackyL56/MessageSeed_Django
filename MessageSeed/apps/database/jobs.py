from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from .models import Message


def delete_expired_messages():
    """ Background job to delete all expired messages"""
    Message.objects.filter(death_date__lt=timezone.now()).delete()


def daily_reset():
    # print("Every Minute")
    pass

def start_scheduler():
    scheduler = BackgroundScheduler(timezone='UTC')
    scheduler.add_job(delete_expired_messages, 'interval', seconds=5)
    # scheduler.add_job(daily_reset, 'cron', minute='0-59')
    scheduler.start()

