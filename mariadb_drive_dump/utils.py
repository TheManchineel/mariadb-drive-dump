import logging
from os import environ, makedirs
from contextlib import contextmanager
from pathlib import Path
from shutil import copy


def get_logger(name, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
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
    config_path = Path(__file__).parents[1] / "config" / "config.ini"
    if not config_path.exists():
        config_example_path = (
            Path(__file__).parents[1] / "config_example" / "config.ini"
        )
        makedirs(config_path.parent, exist_ok=True)
        copy(config_example_path, config_path)
        return True
    return False
