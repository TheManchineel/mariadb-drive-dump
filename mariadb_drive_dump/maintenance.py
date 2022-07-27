from pydrive2.drive import GoogleDriveFile
from datetime import datetime, timedelta
from pytz import UTC
from dateutil import parser

from .google_drive import list_directory
from .config import target_directory_id, retention_days
from .utils import get_logger


def time_of_last_backup() -> datetime:
    files: list[GoogleDriveFile] = list_directory(
        target_directory_id, latest_first=True
    )
    if len(files) == 0:
        return datetime.min
    else:
        return parser.parse(files[0].metadata["createdDate"])


def spring_clean() -> int:
    deleted_count = 0
    files: list[GoogleDriveFile] = list_directory(
        target_directory_id, oldest_first=True
    )
    for file in files:
        if parser.parse(file.metadata["createdDate"]) < (
            UTC.localize(datetime.now() - timedelta(days=retention_days))
        ):
            get_logger().info(f"Deleting old file \"{file.metadata['title']}\"")
            file.Delete()
            deleted_count += 1

    return deleted_count
