import atexit
from apscheduler.schedulers.background import BackgroundScheduler as BgScheduler

class BackgroundScheduler(BgScheduler):

    def __init__(self, gconfig={}, **options):
        super().__init__(gconfig=gconfig, **options)
        atexit.register(lambda: self.shutdown())
