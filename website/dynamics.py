#!/usr/bin/env python

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
"""pydrive_google_drive.py: using pydrive to do general uploading, changing, creating of files on Google Drive."""

# __author__ = "Min Zhou"
# __copyright__ = "Copyright 2019"
# __email__ = "minzhou@bu.edu"


def auth_pydrive():
    """
    Authentication pydrive and only opening browser once using OAuth client ID.
    Returns
    -------
    GoogleDrive object
        authenticated
    """
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("data.csv")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("instance/mycreds.txt")

    drive = GoogleDrive(gauth)
    return drive


def list_all_files(drive, parent_id):
    """
    List all files in Google Drive folder.
    Parameters
    ----------
    drive: GoogleDrive object
    parent_id : str
        Parent folder File ID
    """
    file_list = drive.ListFile(
        {'q': f"'{parent_id}' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))


def find_File_ID(drive, parent_id, filename):
    """
    Find a Google Drive File ID.
    Parameters
    ----------
    drive: GoogleDrive object
    parent_id : str
        Parent folder File ID
    filename : str
        filename of the file to be found
    Returns
    -------
    str
        Google Drive File ID
    None
        if the file doesn't exist
    """
    file_list = drive.ListFile(
        {'q': f"'{parent_id}' in parents and trashed=false"}).GetList()
    if file_list and len(file_list) != 0:
        for file in file_list:
            if filename.lower() == file['title'].lower():
                file_id = file['id']
                return file_id
    return None


def create_folder_if_not_exist(drive, parent_id, folder_name):
    """
    Create a folder on Google Drive if the folder doesn't exist. 
    or return the exiting folder File ID.
    Parameters
    ----------
    drive: GoogleDrive object
    parent_id : str
        parent folder File ID
    folder_name : str
        the name of the folder
    Returns
    -------
    str
        folder File ID on Google Drive
    """
    folder_id = find_File_ID(drive, parent_id, folder_name)
    if not folder_id:
        folder_metadata = {'title': f'{folder_name}',
                           'mimeType': 'application/vnd.google-apps.folder', "parents": [{"id": f'{parent_id}'}]}
        folder = drive.CreateFile(folder_metadata)
        folder.Upload({'convert': True})
        folder_id = folder['id']
    return folder_id


def upload_new_local_file(drive, filename, extention, folder_id):
    """
    Upload a new file to a Google Drive folder from local.
    Parameters
    ----------
    drive: GoogleDrive object
    filename : str
        the name will be used on the Google Drive
    extention: '.pdf', '.txt', '.csv', ...
    folder_id : str
        parent folder File ID
    Returns
    -------
    str
        uploaded file's File ID
    """
    file_metadata = {'title': f'{filename}.pdf',
                     'mimeType': 'application/pdf', "parents": [{"id": f'{folder_id}'}]}
    new_file = drive.CreateFile(file_metadata)
    new_file.SetContentFile(f'/path/to/local_file.pdf')
    new_file.Upload()
    file_id = new_file['id']
    return file_id


def update_file_content(drive, file_id):
    """
    Update a file content of an exiting file on Google Drive.
    Parameters
    ----------
    drive: GoogleDrive object
    file_id : str
        exiting file File ID
    Returns
    -------
    str
        updated file's File ID
    """
    old_file = drive.CreateFile(
        {'id': f"{file_id}", 'mimeType': 'application/pdf'})
    old_file.SetContentFile('/path/to/local_file.pdf')
    old_file.Upload()
    old_file_id = old_file['id']
    return old_file_id