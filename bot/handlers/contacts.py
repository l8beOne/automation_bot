from keyboards import reply_keyboards
from utils import texts
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message


router = Router()
keyboard_contacts = reply_keyboards.contacts_buttons()


@router.message(F.text.lower().in_({"контакты"}))
async def conacts_commands(message: Message):
    '''
    Этот хэндлер обрабатывает кнопку "Контакты".
    '''
    await message.answer(
        text = "Здесь вы можете получить все контакты",
        reply_markup= keyboard_contacts
    )


@router.message(F.text.lower().in_({"учебный офис", "руководители", "учителя"}))
async def process_contacts_commands(message: Message):
    '''
    Этот хэндлер обрабатывает кнопки контактов.
    '''
    for item, contact_dict in texts.NAME_USERNAME.items():
        if message.text.lower() == item:
            content = "".join([f"{username}\n <a>{contacts}</a>\n" for username, contacts in contact_dict.items()])
            await message.answer(
                text = content,
                parse_mode=ParseMode.HTML,
                reply_markup= keyboard_contacts
            )
