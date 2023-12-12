from io import BytesIO
from sys import exit

from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidKey

from .config import encryption_key
from .utils import get_logger


def encrypt_buffer(buffer: BytesIO) -> BytesIO:
    try:
        f = Fernet(encryption_key)
        return BytesIO(f.encrypt(buffer.getvalue()))
    except InvalidKey:
        get_logger(__name__).error("Invalid key. Please check your config file.")
        exit(1)
    except Exception as e:
        get_logger(__name__).error(e)
        exit(1)


def decrypt_buffer(buffer: BytesIO) -> BytesIO:
    try:
        f = Fernet(encryption_key)
        return BytesIO(f.decrypt(buffer.getvalue()))
    except InvalidKey:
        get_logger(__name__).error("Invalid key. Please check your config file.")
        exit(1)
    except Exception as e:
        get_logger(__name__).error(e)
        exit(1)
