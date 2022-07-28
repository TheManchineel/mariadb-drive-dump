from subprocess import check_output, PIPE, CalledProcessError
from io import BytesIO

from .config import (
    mysql_host,
    mysql_port,
    mysql_user,
    mysql_password,
    mysql_databases,
)
from .utils import get_logger, environment_variable, human_readable_size

# Dump all databases to a buffer

mysqldump_arguments = [
    "mysqldump",
    "-u",
    mysql_user,
    "-h",
    mysql_host,
    "-P",
    mysql_port,
    "--single-transaction",
]

if not mysql_databases:
    mysqldump_arguments.append("--all-databases")
else:
    mysqldump_arguments.append("--databases")
    mysqldump_arguments.extend(mysql_databases)


def dump_databases() -> BytesIO:
    logger = get_logger(__name__)
    logger.info("Starting dump")
    try:
        with environment_variable("MYSQL_PWD", mysql_password):
            output = BytesIO(
                check_output(
                    mysqldump_arguments,
                    stderr=PIPE,
                )
            )
            output.seek(0, 2)  # Seek to the end of the buffer
            logger.info(f"Dump successful ({human_readable_size(output.tell())})")
            output.seek(0, 0)  # Seek to the beginning of the buffer
            return output
    except CalledProcessError as e:
        get_logger(__name__).error(f"{e.stderr.decode()}")
