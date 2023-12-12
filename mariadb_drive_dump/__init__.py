__version__ = "0.1.0"

from pycron import has_been
from datetime import datetime, timedelta
from time import sleep

from utils.job import DumpJob
from utils.config import crontab
from utils.maintenance import time_of_last_backup, spring_clean


def launch_job():
    global job
    job = DumpJob()
    job.thread.join()


job: DumpJob = None
last_backup_time: datetime = time_of_last_backup()

ONE_MINUTE = timedelta(minutes=1)

while True:
    if has_been(crontab, last_backup_time):
        last_backup_time = datetime.now()
        launch_job()
        spring_clean()
    else:
        now = datetime.now()
        seconds_until_next_minute = (
            (now + ONE_MINUTE).replace(microsecond=0, second=1) - now
        ).seconds
        sleep(seconds_until_next_minute)
        continue
