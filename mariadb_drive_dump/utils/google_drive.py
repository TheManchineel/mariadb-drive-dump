from __future__ import annotations

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive, GoogleDriveFile, GoogleDriveFileList
from oauth2client.service_account import ServiceAccountCredentials
from io import BytesIO

from utils.config import credentials_path

OAUTH_SCOPE = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.install",
]

FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"

drive = None


class FakeEncodableBytesIO(BytesIO):
    def encode(self, encoding: str = None) -> bytes:
        return self.getvalue()

    @classmethod
    def upgrade(cls, obj: BytesIO) -> FakeEncodableBytesIO:
        return cls(obj.getvalue())


# Helper functions


def get_google_drive() -> GoogleDrive:
    global drive
    if drive is None:
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_path, OAUTH_SCOPE
        )
        drive = GoogleDrive(gauth)
    return drive


def resolve_file(id_or_file: str | GoogleDriveFile) -> GoogleDriveFile:
    drive = get_google_drive()
    if isinstance(id_or_file, str):
        return drive.CreateFile({"id": id_or_file})
    else:
        return id_or_file


def check_file_exists(file: str | GoogleDriveFile) -> bool:
    file = resolve_file(file)
    file.FetchMetadata()
    return file.metadata is not None


def is_directory(file: str | GoogleDriveFile) -> bool:
    file = resolve_file(file)
    file.FetchMetadata()
    return file.metadata["mimeType"] == FOLDER_MIME_TYPE


# Main functions


def list_directory(
    directory: str | GoogleDriveFile,
    latest_first: bool = False,
    oldest_first: bool = False,
) -> GoogleDriveFileList:
    drive = get_google_drive()
    directory: GoogleDriveFile = resolve_file(directory)
    directory.FetchMetadata()
    criteria = {
        "q": "'{}' in parents and trashed=false".format(directory.metadata["id"])
    }
    if latest_first:
        criteria["orderBy"] = "createdDate desc"
    if oldest_first:
        criteria["orderBy"] = "createdDate asc"
    if is_directory(directory):
        return drive.ListFile(criteria).GetList()
    else:
        if check_file_exists(directory):
            raise FileNotFoundError("Not a directory")
        else:
            raise FileNotFoundError("Directory does not exist")


def upload_file(
    parent_directory: str | GoogleDriveFile, file_name: str, file_content: BytesIO
) -> GoogleDriveFile:
    drive = get_google_drive()

    # Check if file already exists
    parent_directory = resolve_file(parent_directory)
    if not is_directory(parent_directory):
        if check_file_exists(parent_directory):
            raise FileNotFoundError("Not a directory")
        else:
            raise FileNotFoundError("Parent directory does not exist")

    parent_children = list_directory(parent_directory)
    for child in parent_children:
        if child.metadata["title"] == file_name:
            raise FileExistsError("File already exists")

    parent = {"id": parent_directory.metadata["id"]}
    item: GoogleDriveFile = drive.CreateFile({"title": file_name, "parents": [parent]})
    file_content = FakeEncodableBytesIO.upgrade(file_content)
    item.SetContentString(file_content)
    item.Upload()
    return item


def download_file(file: str | GoogleDriveFile) -> BytesIO:
    file = resolve_file(file)
    file.FetchMetadata()
    if is_directory(file):
        raise FileNotFoundError("Not a file")
    return BytesIO(file.GetContentIOBuffer().getvalue())


def delete_file(file: str | GoogleDriveFile) -> None:
    file = resolve_file(file)
    file.Trash()
