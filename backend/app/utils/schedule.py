from apscheduler.schedulers.background import BackgroundScheduler
import logging

from app.core.config import settings

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


sched = BackgroundScheduler(timezone="Asia/Kathmandu")
sched.add_jobstore('sqlalchemy', url=settings.SQLALCHEMY_DATABASE_URI)


def schedule_task(func, date):
    # schedule auction ending

    sched.add_job(
        func,
        'date',
        run_date=date
    )
