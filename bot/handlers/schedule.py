import httplib2
import googleapiclient.discovery
import config
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from oauth2client.service_account import ServiceAccountCredentials

router = Router()


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    '''
    Этот хэндлер будет срабатывать на команду "/help"
    '''
    await message.answer(
        'schedule'
    )

@router.message(Command(commands=['schedule']))
async def process_schedule_command(message: Message):
    '''
    Этот хэндлер будет срабатывать на команду "/schedule"
    '''
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
    await message.answer("Какой день?", reply_markup=keyboard)
    




@router.message(F.text.lower() == "ПН")
async def ScheduleForMonday(message: Message):

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

@router.message(F.text.lower() == "ВТ")
async def ScheduleForMonday(message: Message):

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
        range='I8:M12',
        majorDimension='ROWS'
    ).execute().values())[2:][0]

    schedule = []
    for rows in values:
        schedule.append(' '.join(rows))
    await message.answer('\n\n'.join(schedule))

@router.message(F.text.lower() == "СР")
async def ScheduleForMonday(message: Message):

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
