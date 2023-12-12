from pathlib import Path
from configparser import ConfigParser
from os import getenv

if getenv("MARIADB_DRIVE_DUMP_CONFIG_DIR") is not None:
    config_dir_path = Path(getenv("MARIADB_DRIVE_DUMP_CONFIG_DIR"))
else:
    config_dir_path = Path("config")

credentials_path = config_dir_path / "credentials.json"
config_path = config_dir_path / "config.ini"

config = ConfigParser()
config.read(config_path)

target_directory_id = config["Backup"]["target_directory_id"]

encryption_key = config["Backup"]["encryption_key"]
if encryption_key.strip() == "":
    encryption_key = None
else:
    encryption_key = encryption_key.encode()

crontab = config["Backup"]["crontab"]

retention_days = int(config["Backup"]["retention_days"])

mysql_user = config["MySQL"]["user"]
mysql_password = config["MySQL"]["password"]
mysql_host = config["MySQL"]["host"]
mysql_port = config["MySQL"]["port"]
mysql_databases = [
    i.strip() for i in config["MySQL"]["databases"].split(",") if i.strip() != ""
]
