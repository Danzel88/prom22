from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from tgbot.config import load_config

con = load_config('.env')


class GoogleDocReader:
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

    def __init__(self, docs_id: str, cred_file: str):
        self._docs_id = docs_id
        self._cred_file = cred_file
        self._service = self._create_service()

    def _create_service(self):
        cred = service_account.Credentials.from_service_account_file(self._cred_file, scopes=self.SCOPES)
        try:
            return build('docs', 'v1', credentials=cred, cache_discovery=False)
        except HttpError as err:
            print(err)

    def _formater(self, data: str):
        return f'<b>{data[:13]}</b>{data[13::]}'

    def get_data_from_gdocs(self):
        document = self._service.documents().get(documentId=self._docs_id).execute()
        doc_content = document.get('body').get('content')
        events = []
        for val in doc_content:
            if "paragraph" in val:
                events.append(self._formater(val.get('paragraph').get('elements')[0]['textRun']['content']).strip('\n'))
        return events


class GoogleSheetReader:
    SCOPES = ["https://www.googleapis.com/auth/drive.file",
              "https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, sheet_id: str, cred_file: str):
        self._sheet_id = sheet_id
        self._cred_file = cred_file
        self._service = self._create_service()

    def _create_service(self):
        cred = service_account.Credentials.from_service_account_file(self._cred_file, scopes=self.SCOPES)
        try:
            return build('sheets', 'v4', credentials=cred, cache_discovery=False)
        except HttpError as err:
            print(err)

    def get_data_from_gsheet(self, start: int = 2):
        range_ = f"A{start}:E"
        request = self._service.spreadsheets().values().get(spreadsheetId=con.google.chat_sheet_id, range=range_)
        return request.execute()['values']
