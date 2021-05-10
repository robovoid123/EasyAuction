from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


sched = BackgroundScheduler()


def schedule_task(func, date):
    # schedule auction ending

    job = sched.add_job(
        func,
        'date',
        run_date=date
    )

    print(job)
