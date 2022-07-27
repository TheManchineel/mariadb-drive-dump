from pycron import has_been
from datetime import datetime, timedelta
from time import sleep
from signal import signal, SIGINT, SIGTERM

from utils.job import DumpJob
from utils.config import crontab
from utils.maintenance import time_of_last_backup, spring_clean
from utils.utils import get_logger


def launch_job():
    global job
    job = DumpJob()
    job.thread.join()


def on_signal(signal_number, frame):
    del frame
    logger = get_logger(__name__)
    logger.info(f"Received signal {signal_number}")
    global job
    if job is None or job.finished:
        logger.info("No job running, exiting immediately. Goodbye!")
        exit(0)
    else:
        logger.info("Still terminating current backup job, then exiting")
        job.thread.join()
        logger.info("Skipping spring clean routine. Goodbye!")
        exit(0)


signal(SIGINT, on_signal)
signal(SIGTERM, on_signal)

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
