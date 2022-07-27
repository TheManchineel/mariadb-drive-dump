from io import BytesIO
from gzip import GzipFile


def compress_buffer(data: BytesIO) -> BytesIO:
    compressed = BytesIO()
    with GzipFile(fileobj=compressed, mode="wb") as f:
        f.write(data.getvalue())
    compressed.seek(0, 0)
    return compressed


def decompress_buffer(data: BytesIO) -> BytesIO:
    decompressed = BytesIO()
    with GzipFile(fileobj=data, mode="rb") as f:
        decompressed.write(f.read())
    decompressed.seek(0, 0)
    return decompressed
