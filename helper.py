# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
import sys
sys.path.append('lib')

import httplib2
from googleapiclient.discovery import build as discovery_build
from constants import GMAIL_SCOPES, ACCOUNT_SERVICE_KEY_FILE
from oauth2client import service_account



class AccountServiceHelper(object):
    API_SERVICE = None
    API_VERSION = None
    SCOPES = None

    def __init__(self, user_email=None):
        credentials = service_account.ServiceAccountCredentials\
            .from_json_keyfile_name(ACCOUNT_SERVICE_KEY_FILE,
                                    scopes=self.SCOPES)

        credentials = credentials.create_delegated(user_email)
        self.user_email = user_email
        self.http = credentials.authorize(httplib2.Http(timeout=120))
        self.service = discovery_build(self.API_SERVICE, self.API_VERSION,
                                       http=self.http)



class GmailHelper(AccountServiceHelper):
    """ Google Migration API helper class"""
    API_SERVICE = 'gmail'
    API_VERSION = 'v1'
    SCOPES = GMAIL_SCOPES

    def list_messages(self, q, page_token=None):
        params = {'userId': 'me', 'q': q}

        if page_token:
            params['pageToken'] = page_token

        response = self.service.users().messages().list(**params).execute()
        return response.get('messages',[]), response.get('nextPageToken',None)

    def get_label_info(self, label):
        label_info = self.service.users().labels().get(userId='me',
                                                        id=label).execute()
        return label_info




