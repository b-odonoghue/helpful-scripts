# Python script using Google Admin SDK
# to loop through all pages of user info
# have export to csv file

from __future__ import print_function
import httplib2
import os
import pandas as pd
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Directory API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'admin-directory_v1-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_user_list():

    credentials = get_credentials()

    http = credentials.authorize(httplib2.Http())
    df = pd.DataFrame()
    service = discovery.build('admin', 'directory_v1', http=http)
    token_value = ''
    while token_value is not None:
        results = service.users().list(customer='my_customer', maxResults=500,
                                         orderBy='email',pageToken=token_value).execute()
        token_value = results.get('nextPageToken')
        user_info = pd.DataFrame.from_dict(results.get('users',[]))
        df = df.append(user_info)

    df.to_csv('<..>test-outputs/all-user-info.csv',index=False)

if __name__ == '__main__':

    get_user_list()

