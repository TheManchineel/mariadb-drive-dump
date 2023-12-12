__version__ = "0.1.0"

from pycron import has_been
from datetime import datetime, timedelta
from dateutil import parser
from pydrive2.drive import GoogleDriveFile
from time import sleep

from utils.google_drive import list_directory
from utils.job import DumpJob
from utils.config import target_directory_id, crontab


def time_of_last_backup() -> datetime:
    files: list[GoogleDriveFile] = list_directory(
        target_directory_id, latest_first=True
    )
    if len(files) == 0:
        return datetime.min
    else:
        return parser.parse(files[0].metadata["createdDate"])


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
    else:
        now = datetime.now()
        seconds_until_next_minute = (
            (now + ONE_MINUTE).replace(microsecond=0, second=1) - now
        ).seconds
        sleep(seconds_until_next_minute)
        continue
