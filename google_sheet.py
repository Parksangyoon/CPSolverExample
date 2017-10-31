import gspread
from oauth2client.service_account import ServiceAccountCredentials


def read_sheet():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Timetable-f51251aa908e.json', scope)
    client = gspread.authorize(credentials)

    sheet = client.open("시간표").sheet1

    list_of_hashes = sheet.get_all_records()
    for i in list_of_hashes:
        print(i)
