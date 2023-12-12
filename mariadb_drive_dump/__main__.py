from .utils import check_and_fix_config, get_logger

if check_and_fix_config():
    logger = get_logger(__name__)
    logger.warning("Config file not found, created a new one in /config")
    logger.warning("Please edit the config file and restart the program")
    exit(1)

from pycron import is_now, has_been
from datetime import datetime, timedelta
from time import sleep
from signal import signal, SIGINT, SIGTERM

from .job import DumpJob
from .config import crontab
from .maintenance import time_of_last_backup, spring_clean


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


def launch_job():
    global job
    job = DumpJob()
    job.thread.join()


def main():
    last_backup_time: datetime = time_of_last_backup()
    while True:
        if (
            datetime.now().replace(microsecond=0, second=0)
            != last_backup_time.replace(microsecond=0, second=0)
            and has_been(crontab, last_backup_time)
            and not (
                datetime.now().replace(microsecond=0, second=0)
                == last_backup_time.replace(microsecond=0, second=0)
                + timedelta(minutes=1)
                and not is_now(crontab)
            )
        ):
            last_backup_time = datetime.now()
            launch_job()
            spring_clean()
        else:
            sleep(1)
            continue


main()
