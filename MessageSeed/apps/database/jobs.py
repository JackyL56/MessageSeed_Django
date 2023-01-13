from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from .helper import *
from .models import Message


def daily_reset():
    pass


def delete_expired_messages():
    """ Background job to delete all expired messages"""
    for msg in Message.objects.filter(state__lt=Helper.DEAD, death_date__lt=timezone.now()):
        msg.state = Helper.DEAD
        msg.save()


def check_evolve():
    for msg in Message.objects.filter(state__lt=Helper.TREE):
        m_lifetime_days = msg.current_lifetime.days
        if m_lifetime_days >= Helper.STATE_EVOLVE_THRESHOLD.get(msg.state):
            msg.evolve()
            if msg.state == Helper.SAPLING:
                msg.author.add_experience(Helper.EXPERIENCE_EVOLVED_TO_SAPLING)
            else:
                msg.author.add_experience(Helper.EXPERIENCE_EVOLVED_TO_TREE)


def start_scheduler():
    scheduler = BackgroundScheduler(timezone='UTC')
    scheduler.add_job(delete_expired_messages, 'interval', seconds=30)
    scheduler.add_job(check_evolve, 'cron', hour='*')
    scheduler.start()

