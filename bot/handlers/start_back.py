from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import Bold, Text
from asyncpg.exceptions import UniqueViolationError

from keyboards import reply_keyboards
from utils.database_connect import Request
from utils.texts import TEXT_FOR_HELP_COMMAND
from utils.user_status_class import UserStatusClass

router = Router()
keyboard_start_buttons = reply_keyboards.start_buttons()


@router.message(Command(commands=["start"]))
async def process_start_commands(
    message: Message, request: Request, userstatus: UserStatusClass
):
    """
    Этот хэндлер будет срабатывать на команду "/start".
    """
    user_id = message.from_user.id
    if not await request.check_table("user_status"):
        await request.create_user_status_table("user_status")
    try:
        await userstatus.add_user("user_status", user_id)
        content = Text(
            "Привет, ",
            Bold(message.from_user.full_name),
            ". Здесь Вы можете получить ваше расписание и "
            "ответы на вопросы касающиеся учебного офиса.",
        )
        await message.answer(
            **content.as_kwargs(),
            reply_markup=keyboard_start_buttons
        )
    except UniqueViolationError:
        await message.answer(
            "Вы уже зарегестрированы в боте!",
            reply_markup=keyboard_start_buttons
        )
    await message.answer(
        "Подробнее с правилами бота вы можете ознакомиться "
        "написав/выбрав команду /help"
    )


@router.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    """
    Этот хэндлер будет срабатывать на команду "/help"
    """
    await message.answer(TEXT_FOR_HELP_COMMAND)


@router.message(F.text.lower().in_({"назад"}))
async def back_command(message: Message, state: FSMContext):
    """
    Этот хэндлер будет срабатывать на кнопку "Назад".
    """
    await message.answer(
        text="Вы вернулись в главное меню", reply_markup=keyboard_start_buttons
    )
    await state.clear()
