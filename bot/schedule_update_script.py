import httplib2
import googleapiclient.discovery
import config
import json
import sched, time
from oauth2client.service_account import ServiceAccountCredentials

days_ranges = {'ПАДИИ 1' : {'ПН': 'J3:M11', 'ВТ': 'J13:M21', 'СР': 'J23:M31', 'ЧТ': 'J33:M43', 'ПТ': 'J45:M52', 'СБ': 'J54:M61'}
            , 'ПМИ 1' : {'ПН': 'C3:F11', 'ВТ': 'C13:F21', 'СР': 'C23:F31', 'ЧТ': 'C33:F43', 'ПТ': 'C45:F52', 'СБ': 'C54:F61'}
            , 'ПАДИИ 2' : {'ПН': 'J3:M11', 'ВТ': 'J13:M21', 'СР': 'J23:M33', 'ЧТ': 'J35:M44', 'ПТ': 'J46:M54', 'СБ': 'J56:M63'}
            , 'ПМИ 2' : {'ПН': 'C3:F11', 'ВТ': 'C13:F21', 'СР': 'C23:F33', 'ЧТ': 'C35:F44', 'ПТ': 'C46:F54', 'СБ': 'C56:F63'}
            }

scheduler_ = sched.scheduler(time.time, time.sleep)
def f():
    scheduler_.enter(60, 1, f)  #Обновляется раз в 600 секунд
    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        config.CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

    # Получаем информацию обо всех листах в таблице sheets[1]['properties']['title']
    spreadsheet = service.spreadsheets().get(spreadsheetId=config.spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])
    sheets_number = [' ', sheets[3]['properties']['title'], sheets[4]['properties']['title']]
    schedule_upd = {'ПАДИИ 1' : {'ПН': 'J3:M11', 'ВТ': 'J13:M21', 'СР': 'J23:M31', 'ЧТ': 'J33:M43', 'ПТ': 'J45:M52', 'СБ': 'J54:M61'}
                , 'ПМИ 1' : {'ПН': 'C3:F11', 'ВТ': 'C13:F21', 'СР': 'C23:F31', 'ЧТ': 'C33:F43', 'ПТ': 'C45:F52', 'СБ': 'C54:F61'}
                , 'ПАДИИ 2' : {'ПН': 'J3:M11', 'ВТ': 'J13:M21', 'СР': 'J23:M33', 'ЧТ': 'J35:M44', 'ПТ': 'J46:M54', 'СБ': 'J56:M63'}
                , 'ПМИ 2' : {'ПН': 'C3:F11', 'ВТ': 'C13:F21', 'СР': 'C23:F33', 'ЧТ': 'C35:F44', 'ПТ': 'C46:F54', 'СБ': 'C56:F63'}
                }
    
    for op_course_update in ['ПАДИИ 1', 'ПМИ 1', 'ПАДИИ 2', 'ПМИ 2']:  
        sheet_course = sheets_number[int(op_course_update[-1])]  
        for day_update in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']:
            day_range = days_ranges[op_course_update][day_update]   
            values = list(service.spreadsheets().values().get(
                spreadsheetId=config.spreadsheet_id,
                range=f'{sheet_course}!{day_range}',
                majorDimension='ROWS'
            ).execute().values())[2:][0]

            schedule = []
            for rows in values:
                s = '\n'.join(rows)
                if s.strip() != '':
                    schedule.append(' '.join(rows))
            schedule_upd[op_course_update][day_update] = '\n------------------------\n'.join(schedule)

    with open('schedule.json', 'w', encoding='utf-8') as S:
        json.dump(schedule_upd, S, ensure_ascii=False, indent=4)

f()
scheduler_.run()