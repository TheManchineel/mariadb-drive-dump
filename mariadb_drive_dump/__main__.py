from utils.utils import check_and_fix_config, get_logger

if check_and_fix_config():
    logger = get_logger(__name__)
    logger.warning("Config file not found, created a new one in /config")
    logger.warning("Please edit the config file and restart the program")
    exit(1)

from pycron import has_been
from datetime import datetime, timedelta
from time import sleep
from signal import signal, SIGINT, SIGTERM

from utils.job import DumpJob
from utils.config import crontab
from utils.maintenance import time_of_last_backup, spring_clean


job: DumpJob = None


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


ONE_MINUTE = timedelta(minutes=1)


def launch_job():
    global job
    job = DumpJob()
    job.thread.join()


def main():
    last_backup_time: datetime = time_of_last_backup()
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


main()
