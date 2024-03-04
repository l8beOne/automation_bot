import keyboards
from aiogram import Router, F
from aiogram.types import Message


router = Router()

@router.message(F.text.lower() == "информация про вышку")
async def hse_info_commands(message: Message):
    '''
    Этот хэндлер обрабатывает кнопки начального меню.
    '''
    await message.answer(
        text = "Здесь вы можете получить информацию и гайд по Вышке",
        reply_markup= await keyboards.hse_info_buttons()
    )
