from configparser import ConfigParser
from .utils import get_config_dir_path

config_dir_path = get_config_dir_path()

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

database_type = config["Backup"]["database_type"]

mysql_user = config["MySQL"]["user"]
mysql_password = config["MySQL"]["password"]
mysql_host = config["MySQL"]["host"]
mysql_port = config["MySQL"]["port"]
mysql_databases = [
    i.strip() for i in config["MySQL"]["databases"].split(",") if i.strip() != ""
]

postgres_user = config["PostgreSQL"]["user"]
postgres_password = config["PostgreSQL"]["password"]
postgres_host = config["PostgreSQL"]["host"]
postgres_port = config["PostgreSQL"]["port"]
postgres_skip_databases = config["PostgreSQL"]["skip_databases"]
