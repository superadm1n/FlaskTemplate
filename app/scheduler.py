import atexit
from apscheduler.schedulers.background import BackgroundScheduler


def start_schedule(app):
    scheduler = BackgroundScheduler()
    #scheduler.add_job(func=trace_cameras, trigger="cron", hour='*/12', args=(app,))
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    return scheduler
