from keyboards import reply_keyboards
from utils import texts
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message


router = Router()
keyboard_hse_info_buttons = reply_keyboards.hse_info_buttons()

@router.message(F.text.lower().in_({"информация про вышку"}))
async def hse_info_commands(message: Message):
    '''
    Этот хэндлер обрабатывает кнопку "Информация про вышку".
    '''
    await message.answer(
        text = "Здесь вы можете получить информацию и гайд по Вышке",
        reply_markup= keyboard_hse_info_buttons
    )


@router.message(F.text.lower().in_({"гайд по вышке", "академический отпуск", "отчисление"}))
async def process_contacts_commands(message: Message):
    '''
    Этот хэндлер обрабатывает кнопки инорфмации о вышке.
    '''
    for item, text in texts.BUTTON_INFO.items():
        if message.text.lower() == item:
            await message.answer(
                text = text,
                parse_mode=ParseMode.HTML,
                reply_markup= keyboard_hse_info_buttons
            )
