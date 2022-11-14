# mariadb-drive-dump

Regularly and automatically dump MariaDB, MySQL and PostgreSQL databases to Google Drive with a simple Docker container, with encryption, compression, backup retention management and `cron`-based scheduling built-in.

This simple, although carefully assembled collection of scripts is intended for my own personal use, however I decided to make it public in case anyone might find it useful. It's provided with **ABSOLUTELY NO WARRANTY**, meaning that if you use this and end up losing your data I won't be liable nor will I be able to help you.

## Set-up (Docker)

The easiest way to get this running is Docker.

First and foremost, create a Google Service Account with access to the Drive API and share a directory to it with `Editor` access (see [this guide up to step 4](https://web.archive.org/web/20220522195545/https://www.labnol.org/google-api-service-account-220404) for how to proceed).

Now create a directory on your server (e.g. `/var/mariadb_drive_dump/`) and in it put the following files:
 * `credentials.json`, which you obtained from Google Cloud Console after creating the Google Service Account
 * `config.ini`, based on the template from [here](https://github.com/TheManchineel/mariadb-drive-dump/blob/master/mariadb_drive_dump/config/config.ini)

It's particularly important that you pay attention to:

 * `crontab` to set the interval of recurring backups (refer to https://crontab.guru for help finding the optimal crontab)
 * `target_directory_id`, which must be the proper Google Drive directory ID (e.g. the ID of the directory at the URL `https://drive.google.com/drive/folders/13jac_avcEjeD2CAw13Flk1x3g0QghG21` is `13jac_avcEjeD2CAw13Flk1x3g0QghG21`
 * `database_type`, set to either `mysql` (MySQL or MariaDB databases) or `postgres` (PostgreSQL databases)
 * all the options in the section (`[MySQL]` or `[PostgreSQL]`) corresponding to your database engine of choice, leaving the other untouched; pay attention to the different behavior of `databases` and `skip_databases`, respectively only available for MySQL/MariaDB and for PostgreSQL

If you wish to use encryption, set encryption_key to a valid Fernet key. To generate one, you must have Python 3 installed on your computer as well as the `cryptography` module (`pip3 install cryptography`). You can then enter the following in your Python shell:

```python
from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())
```

Finally, you can start the Docker container with:

```sh
docker run -v /var/mariadb_drive_dump/:/config/ -d --name mariadb_drive_dump manchineel/mariadb_drive_dump
```

You can monitor the container with `docker logs mariadb_drive_dump` and start/stop it with the usual `docker start` and `docker stop` commands.

To decrypt the encrypted sql.gz files, you'll have to run the decrypt.py script in this repository. A neater, automated solution will be coming with a later update.
