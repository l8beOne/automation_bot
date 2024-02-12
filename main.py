import httplib2
import apiclient.discovery
import config
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from oauth2client.service_account import ServiceAccountCredentials


# Создаем объекты бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Здарова')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'schedule'
    )
# Этот хэндлер будет срабатывать на команду "/schedule"
@dp.message(Command(commands=['schedule']))
async def process_schedule_command(message: Message):
    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        config.CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    # Пример чтения файла
    values = service.spreadsheets().values().get(
        spreadsheetId=config.spreadsheet_id,
        range='H1:M12',
        majorDimension='COLUMNS'
    ).execute()
    await message.answer(str(values))

# Этот хэндлер будет срабатывать на любые текстовые сообщения (кроме /start /help /schedule)
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)
