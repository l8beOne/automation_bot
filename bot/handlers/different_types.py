from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def different_types(message: Message):
    await message.answer("Я не умею обрабатывать такого рода сообщения.")
