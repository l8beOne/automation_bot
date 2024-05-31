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
        # Пример чтения файла    
        values = list(service.spreadsheets().values().get(
            spreadsheetId=config.spreadsheet_id,
            range=f'{sheet_course}!I2:M12',
            majorDimension='ROWS'
        ).execute().values())[2:][0]

        schedule = []
        for rows in values:
            schedule.append(' '.join(rows))
        await message.answer('\n\n'.join(schedule))
        await message.answer(f' день: {op_course_day["day"]}')
    else:
        await message.answer(
            text = "Вы вернулись в главное меню",
            reply_markup= keyboard_start_buttons
        )
        await state.clear()
    
