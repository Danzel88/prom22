import string

from googleapiclient import discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials




#debug data
from tgbot.config import load_config
config = load_config('.env')
val = [['1', 'Parrent', 'Den, 1', "All event super cool!!!!"],
       ['2', 'Teacher', 'John, 2', "All event super cool!!!!"]]


class GoogleWriter:
    review_headers = [['Tg ID', 'Роль', 'Имя', 'Школа', 'Отзыв']]
    chat_sheet_headers = [['Tg ID', 'Имя','Класс', 'Школа', 'Сообщение']]
    sticker_pack_headers = [['Tg ID', 'Имя', 'Фраза']]

    def __init__(self, spreadsheet_id: str, cred_file: str, ):
        self._spreadsheet_id = spreadsheet_id
        self.__cred_file = cred_file
        self._service = self._service_builder()

    def _check_header(self, coll_quantity: str) -> dict:
        return self._service.spreadsheets().values().get(spreadsheetId=self._spreadsheet_id,
                                                         range=f'{coll_quantity[0]}1:{coll_quantity[-1]}1',
                                                         majorDimension="ROWS").execute()

    def _create_sheets_header(self, coll_letter: str):
        headers = None
        match self._spreadsheet_id:
            case config.google.review_sheet_id:
                headers = self.review_headers
            case config.google.chat_sheet_id:
                headers = self.chat_sheet_headers
            case config.google.stickerpack_sheet_id:
                headers = self.sticker_pack_headers
        self._service.spreadsheets().values().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f'{coll_letter[0]}1:{coll_letter[-1]}1',
                     "majorDimension": "ROWS",
                     "values": headers}]})\
            .execute()

    def _service_builder(self):
        credential = ServiceAccountCredentials. \
            from_json_keyfile_name(self.__cred_file,
                                   ["https://www.googleapis.com/auth/drive.file",
                                    "https://www.googleapis.com/auth/spreadsheets"]
                                   )
        http_auth = credential.authorize(httplib2.Http())
        return discovery.build("sheets", "v4", http=http_auth, cache_discovery=False)

    def data_writer(self, data, coll_quantity: int):
        coll_letter = string.ascii_uppercase[:coll_quantity]
        if self._check_header(coll_letter).get('values') is None:
            self._create_sheets_header(coll_letter)
        self._service.spreadsheets().values().append(
            spreadsheetId=self._spreadsheet_id,
            range=f'{coll_letter[0]}:{coll_letter[-1]}',
            valueInputOption="USER_ENTERED",
            body={"majorDimension": "ROWS",
                  "values": data}).execute()


# test = GoogleWriter(config.google.review_sheet_id, config.google.cred_file)
# test.data_writer(val, len(val[0]))
