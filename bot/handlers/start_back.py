import keyboards
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.formatting import Text, Bold
from aiogram.types import Message


router = Router()


@router.message(Command(commands=["start"]))
async def process_start_commands(message: Message):
    '''
    Этот хэндлер будет срабатывать на команду "/start".
    '''
    content = Text(
        f"Привет, ",
        Bold(message.from_user.full_name),
        f". Здесь Вы можете получить ваше расписание и ответы на вопросы касающиеся учебного офиса."
    )
    await message.answer(
        **content.as_kwargs(),
        reply_markup= await keyboards.start_buttons()
    )


@router.message(F.text.lower() == "назад")
async def back_command(message: Message):
    '''
    Этот хэндлер будет срабатывать на кнопку "Назад".
    '''
    await message.answer(
        text = "Вы вернулись назад",
        reply_markup= await keyboards.start_buttons()
    )
