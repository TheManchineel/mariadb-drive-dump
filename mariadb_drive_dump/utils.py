import logging
from os import environ, makedirs, getenv
from contextlib import contextmanager
from pathlib import Path
from shutil import copy


def get_config_dir_path() -> Path:
    if getenv("MARIADB_DRIVE_DUMP_CONFIG_DIR") is not None:
        return Path(getenv("MARIADB_DRIVE_DUMP_CONFIG_DIR"))
    else:
        return Path("config")


loggers = {}


def get_logger(name: str, level=logging.INFO) -> logging.Logger:
    if loggers.get(name):
        return loggers.get(name)
    else:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
        loggers[name] = logger

        return logger


@contextmanager
def environment_variable(key: str, value: str):
    old_value = environ.get(key)
    environ[key] = value
    yield
    if old_value is None:
        del environ[key]
    else:
        environ[key] = old_value


def human_readable_size(size: int | float, decimal_places: int = 2) -> str:
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def check_and_fix_config() -> bool:
    config_path = get_config_dir_path() / "config.ini"
    if not config_path.exists():
        config_example_path = Path(__file__).parent / "config" / "config.ini"
        makedirs(config_path.parent, exist_ok=True)
        copy(config_example_path, config_path)
        return True
    return False
