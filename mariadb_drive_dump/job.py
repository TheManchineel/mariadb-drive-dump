from datetime import datetime
from threading import Thread

from .config import target_directory_id, encryption_key
from .google_drive import upload_file
from .dump import dump_databases
from .crypto import encrypt_buffer
from .gzip import compress_buffer
from .utils import get_logger


class DumpJob:
    @property
    def timestamp(self):
        return self.start_time.strftime("%Y-%m-%d_%H_%M_%S")

    def __init__(self):
        self.start_time = datetime.now()
        self.thread = Thread(target=lambda: dump_job(self.timestamp))
        self.thread.start()

    @property
    def finished(self):
        return not self.thread.is_alive()


def dump_job(timestamp) -> bool:
    try:
        buffer = compress_buffer(dump_databases())

        if encryption_key is not None:
            buffer = encrypt_buffer(buffer)
            filename = f"encrypted_dump_{timestamp}.sql.gz"
        else:
            filename = f"dump_{timestamp}.sql.gz"

        id = upload_file(target_directory_id, filename, buffer).metadata["id"]
        get_logger(__name__).info(
            f"Dump {filename} successfully uploaded to Google Drive (https://drive.google.com/file/d/{id}/view)"
        )

    except Exception as e:
        get_logger(__name__).error(f"{e}")
