from typing import List

from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
from handlers.schedule_tracking import (
    check_for_certificate_readiness,
    check_for_updates,
)
from utils.states import CertificateFormSteps
from utils.texts import CERTIFICATE_TEXT
from utils.user_status_class import UserStatusClass

router = Router()


@router.message(F.text.lower().in_({"заказать справку"}))
async def certificate_commands(message: Message):
    """
    Этот хэндлер обрабатывает кнопку "Заказать справку".
    """
    await message.answer(text=CERTIFICATE_TEXT, parse_mode=ParseMode.HTML)


@router.message(Command(commands=["full_name_for_certificate"]))
async def suggestion_of_getting_full_name(message: Message):
    """
    Этот хэндлер обрабатывает команду /full_name_for_certificate".
    """
    await message.answer(
        ("Напишите свое ФИО, чтобы автоматически получать "
         "уведовление о готовности справки!"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="Написать", callback_data="write_name"
                )],
                [InlineKeyboardButton(text="Позже", callback_data="later")],
            ]
        ),
    )


@router.callback_query(F.data.in_(["write_name", "later"]))
async def selection(call: CallbackQuery, state: FSMContext):
    """
    Этот хэндлер обрабатывает ответ пользователя
    на команду /full_name_for_certificate.
    """
    if call.data == "write_name":
        await call.message.edit_text("Жду ваше ФИО!")
        await state.set_state(CertificateFormSteps.get_full_name)
    elif call.data == "later":
        await call.message.edit_text(
            "Хорошо, вы в любой момент можете вернуться и заполнить ФИО!",
            reply_markup=None,
        )
        await state.clear()


@router.message(CertificateFormSteps.get_full_name)
async def write_full_name(
    message: Message,
    bot: Bot,
    userstatus: UserStatusClass,
    state: FSMContext,
    apscheduler: AsyncIOScheduler,
):
    """
    Этот хэндлер обрабатывает введеные пользователем ФИО и
    запускает функцию для автоматических уведомлений о готовности справки".
    """
    await userstatus.add_user_full_name(
        "user_status", message.text, message.from_user.id
    )
    await message.answer(
        "Ваши данные записаны, теперь вы будете получать "
        "уведомления о готовности справок! "
        "В случае ошибки в написании ФИО, пройдите эту процедуру еще раз."
    )
    await state.clear()
    user_id = await userstatus.get_user_id("user_status", message.from_user.id)
    certificate_user_names: List[List[str]] = await check_for_updates(
        config.CERTIFICATE_USER_NAME
    )
    await check_for_certificate_readiness(
        bot, user_id, certificate_user_names, userstatus, apscheduler
    )
