from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def send_echo(message: Message):
    '''
    Этот хэндлер будет срабатывать на любые текстовые сообщения (кроме /start /help /schedule)
    '''
    await message.reply(text=message.text)
