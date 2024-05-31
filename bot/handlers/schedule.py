import httplib2
import googleapiclient.discovery
import config
from keyboards import reply_keyboards
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from oauth2client.service_account import ServiceAccountCredentials
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()
op_course_keyboard = reply_keyboards.schedule_op_course_buttons()
day_selection_keyboard = reply_keyboards.schedule_day_buttons()
keyboard_start_buttons = reply_keyboards.start_buttons()

class Schedule(StatesGroup):
    op_course = State()
    day = State()

@router.message(F.text.lower().in_({"узнать расписание"}))
async def process_schedule_command(message: Message, state: FSMContext):
    '''
    Этот хэндлер обрабатывает кнопку "Расписание".
    '''
    await state.set_state(Schedule.op_course)
    await message.answer("Выбор оп и курса", reply_markup=op_course_keyboard)
    
@router.message(Schedule.op_course)
async def ScheduleForMonday(message: Message, state: FSMContext):
    await state.update_data(op_course=message.text)
    await state.set_state(Schedule.day)
    await message.answer("Выбор дня", reply_markup=day_selection_keyboard)
    


@router.message(Schedule.day)
async def ScheduleForMonday(message: Message, state: FSMContext):
    await state.update_data(day=message.text)
    op_course_day = await state.get_data()
    days_ranges = {'ПАДИИ 1' : {'ПН': 'J3:M11', 'ВТ': 'J13:M21', 'СР': 'J23:M31', 'ЧТ': 'J33:M43', 'ПТ': 'J45:M52', 'СБ': 'J54:M61'}
               , 'ПМИ 1' : {'ПН': 'C3:F11', 'ВТ': 'C13:F21', 'СР': 'C23:F31', 'ЧТ': 'C33:F43', 'ПТ': 'C45:F52', 'СБ': 'C54:F61'}
               , 'ПАДИИ 2' : {'ПН': 'J3:M11', 'ВТ': 'J13:M21', 'СР': 'J23:M33', 'ЧТ': 'J35:M44', 'ПТ': 'J46:M54', 'СБ': 'J56:M63'}
               , 'ПМИ 2' : {'ПН': 'C3:F11', 'ВТ': 'C13:F21', 'СР': 'F23:F33', 'ЧТ': 'C35:F44', 'ПТ': 'C46:F54', 'СБ': 'C56:F63'}
               }
    if op_course_day["day"] in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']:
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
        sheet_course= sheets_number[int(op_course_day["op_course"][-1])]
        day_range = days_ranges[op_course_day["op_course"]][op_course_day["day"]]
        # Пример чтения файла    
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
        await message.answer(f'Расписание на {op_course_day["day"]} \n\n' + 
                             '\n--------------------------------------------------------------------\n'.join(schedule))
    else:
        await message.answer(
            text = "Вы вернулись в главное меню",
            reply_markup= keyboard_start_buttons
        )
        await state.clear()
    
