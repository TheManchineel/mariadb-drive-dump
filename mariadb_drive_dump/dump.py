from subprocess import check_output, PIPE, CalledProcessError
from io import BytesIO

from .config import (
    database_type,
    mysql_host,
    mysql_port,
    mysql_user,
    mysql_password,
    mysql_databases,
    postgres_host,
    postgres_port,
    postgres_user,
    postgres_password,
    postgres_skip_databases,
)
from .utils import get_logger, environment_variable, human_readable_size

# Dump all databases to a buffer


def dump_databases() -> BytesIO:
    if database_type == "mysql":
        dump_arguments = [
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
            dump_arguments.append("--all-databases")
        else:
            dump_arguments.append("--databases")
            dump_arguments.extend(mysql_databases)
    elif database_type == "postgres":
        dump_arguments = [
            "pg_dumpall",
            "-U",
            postgres_user,
            "-h",
            postgres_host,
            "-p",
            postgres_port,
        ]
        if postgres_skip_databases:
            dump_arguments.append(f"--exclude-database={postgres_skip_databases}")
    else:
        raise ValueError(f"Unknown database type: {database_type}")
    logger = get_logger(__name__)
    logger.info("Starting dump")
    try:
        if database_type == "mysql":
            env = ["MYSQL_PWD", mysql_password]
        elif database_type == "postgres":
            env = ["PGPASSWORD", postgres_password]
        else:
            raise ValueError(f"Unknown database type: {database_type}")
        with environment_variable(*env):
            output = BytesIO(
                check_output(
                    dump_arguments,
                    stderr=PIPE,
                )
            )
            output.seek(0, 2)  # Seek to the end of the buffer
            logger.info(f"Dump successful ({human_readable_size(output.tell())})")
            output.seek(0, 0)  # Seek to the beginning of the buffer
            return output
    except CalledProcessError as e:
        get_logger(__name__).error(f"{e.stderr.decode()}")
