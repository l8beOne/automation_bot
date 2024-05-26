import httplib2
import googleapiclient.discovery
import config
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from oauth2client.service_account import ServiceAccountCredentials
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()


class Schedule(StatesGroup):
    op_course = State()
    day = State()

@router.message(F.text.lower().in_({"узнать расписание"}))
async def process_schedule_command(message: Message, state: FSMContext):
    '''
    Этот хэндлер обрабатывает кнопку "Расписание".
    '''

    await state.set_state(Schedule.op_course)

    kb = [
        [
            KeyboardButton(text="ПАДИИ 1"),
            KeyboardButton(text="ПМИ 1")
        ],
        [
            KeyboardButton(text="ПАДИИ 2"),
            KeyboardButton(text="ПМИ 2")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="ОП Курс"
    )
    await message.answer("Выбор оп и курса", reply_markup=keyboard)
    
@router.message(Schedule.op_course)
async def ScheduleForMonday(message: Message, state: FSMContext):
    await state.update_data(op_course=message.text)
    await state.set_state(Schedule.day)
    kb = [
        [
            KeyboardButton(text="ПН"),
            KeyboardButton(text="ВТ"),
            KeyboardButton(text="СР"),
            KeyboardButton(text="ЧТ"),
            KeyboardButton(text="ПТ"),
            KeyboardButton(text="СБ")
        ],     
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="День"
    )
    await message.answer("Выбор дня", reply_markup=keyboard)


#@router.message(F.text.lower().in_({"пн"}))
@router.message(Schedule.day)
async def ScheduleForMonday(message: Message, state: FSMContext):
    await state.update_data(day=message.text)
    op_course_day = await state.get_data()

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        config.CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

    # Пример чтения файла    
    values = list(service.spreadsheets().values().get(
        spreadsheetId=config.spreadsheet_id,
        range='I2:M12',
        majorDimension='ROWS'
    ).execute().values())[2:][0]

    schedule = []
    for rows in values:
        schedule.append(' '.join(rows))
    await message.answer('\n\n'.join(schedule))
    await message.answer(f' день: {op_course_day["day"]}')
    await state.clear()
