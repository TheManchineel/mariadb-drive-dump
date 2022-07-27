from io import BytesIO
from gzip import GzipFile

from .utils import get_logger


def compress_buffer(data: BytesIO) -> BytesIO:
    compressed = BytesIO()
    with GzipFile(fileobj=compressed, mode="wb") as f:
        f.write(data.getvalue())
    compressed.seek(0, 0)
    get_logger(__name__).info("Compressed file!")
    return compressed


def decompress_buffer(data: BytesIO) -> BytesIO:
    decompressed = BytesIO()
    with GzipFile(fileobj=data, mode="rb") as f:
        decompressed.write(f.read())
    decompressed.seek(0, 0)
    get_logger(__name__).info("Decompressed file!")
    return decompressed
