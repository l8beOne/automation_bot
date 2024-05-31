import asyncio

from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import config
from filters.is_admin_filter import IsAdminFilter
from filters.user_only import IsUserOnlyFilter
from keyboards.inline_keyboards import (
    ContinueStopDialogAction,
    get_question_response_buttons_keyboard,
)
from utils.database_connect import Request
from utils.response_to_question_class import QuestionResponse
from utils.states import DialogSteps
from utils.user_status_class import UserStatusClass

router = Router()


@router.message(IsUserOnlyFilter(), DialogSteps.start_dialog)
async def start_dialog(
    message: Message,
    bot: Bot,
    state: FSMContext,
    questionresponse: QuestionResponse
):
    """
    Этот хэндлер обрабатывает диалог пользователя с админом,
    если пользователя не удовлетворил ответ админа на вопрос.
    """
    data = await state.get_data()
    response_admin_id = data.get("response_admin_id")
    question_id = data.get("question_id")
    if response_admin_id != 0:
        question = await questionresponse.get_question_from_db(
            "question_response", question_id
        )
        await bot.send_message(
            response_admin_id,
            f"Пользователь <b>({message.from_user.id}) "
            f"{message.from_user.full_name}"
            f"</b> хочет уточнить ответ на счет вопроса: "
            f"<i>``{question}``</i>\r\n\r\n "
            f"<i>'{message.text}'</i>",
            parse_mode=ParseMode.HTML,
        )
    else:
        admin_id = (
            await questionresponse.get_admin_id_dialog_unformed_answer(
                "question_response", message.from_user.id
            )
        )
        await bot.send_message(
            admin_id,
            f"Пользователь <b>({message.from_user.id}) "
            f"{message.from_user.full_name}</b> хочет уточнить: "
            f"<i>'{message.text}'</i>",
            parse_mode=ParseMode.HTML,
        )


@router.message(IsUserOnlyFilter(), F.text.contains("?"))
async def get_question(
    message: Message,
    request: Request,
    questionresponse: QuestionResponse,
    bot: Bot,
    userstatus: UserStatusClass,
):
    """
    Этот хэндлер получает вопрос пользоваетеля
    и пересылает его админу в случае,
    если ответа на этот вопрос еще нет в базе данных.
    """
    symbols_to_remove = ",!.:"
    text = message.text.replace("?", "")
    for symbol in symbols_to_remove:
        text = text.replace(symbol, "")
    if len(text) > 1:
        if not await request.check_table("question_response"):
            await request.create_question_response_table("question_response")
        user_status = await userstatus.get_user_status(
            "user_status", message.from_user.id
        )
        if user_status != "muted":
            if await questionresponse.check_question_in_db(
                "question_response", message.text
            ):
                response = await questionresponse.get_response_from_db(
                    "question_response", message.text
                )
                if (
                    response
                    == (
                        "Данный вопрос уже находится на рассмотрении у "
                        "учебного офиса, ожидайте ответа"
                    )
                ):
                    await message.answer(
                        f"<b>{response}</b>", parse_mode=ParseMode.HTML
                    )
                    await asyncio.sleep(600)
                    return await get_question(
                        message, request, questionresponse, bot
                    )
                else:
                    (
                        question_id,
                        response_admin_id,
                    ) = await questionresponse.get_admin_id_dialog_formed_answer(
                        "question_response", message.text
                    )
                    await message.answer(
                        f"Ответ на вопрос <i>'{message.text}'</i>:\r\n "
                        f"<b>{response}</b>",
                        parse_mode=ParseMode.HTML,
                    )
                    await message.answer(
                        "Вы довольны ответом?",
                        reply_markup=get_question_response_buttons_keyboard(
                            response_admin_id, question_id
                        ),
                    )
            else:
                await message.answer(
                    ("<i>Я еще не умею отвечать на такой вопрос, "
                     "зову сотрудника учебного офиса!</i>"),
                    parse_mode=ParseMode.HTML,
                )
                await questionresponse.add_question(
                    "question_response",
                    message.from_user.id,
                    message.message_id,
                    message.text,
                )
                for admin_id in config.ADMIN_IDS:
                    await bot.send_message(
                        admin_id,
                        f"Пользователь <b>{message.from_user.full_name} "
                        f"({message.from_user.username})</b> задал вопрос: "
                        f"<i>'{message.text}'</i>",
                        parse_mode=ParseMode.HTML,
                    )
        else:
            await message.answer("Вы замьючены и не можете писать сообщения!")
            return
    else:
        await message.answer("Опишите ваш вопрос более конкретно.")


@router.message(IsAdminFilter())
async def get_response_from_admin(
    message: Message, bot: Bot, questionresponse: QuestionResponse
):
    """
    Этот хэндлер получает ответ от админа на вопрос пользоваетеля
    и пересылает его пользователю, при этом занося этот ответ в базу данных.
    """
    if message.text.split()[0] != "/mute":
        try:
            if "задал вопрос" in message.reply_to_message.text:
                question = (
                    message.reply_to_message.text.split("'")[1].strip("'")
                )
                question_id_in_chat = message.reply_to_message.message_id
                user_id = await questionresponse.get_user_id_for_reply(
                    "question_response", question
                )
                await bot.send_message(
                    user_id,
                    f"Ответ на вопрос <i>'{question}'</i>:\r\n "
                    f"<b>{message.text}</b>",
                    parse_mode=ParseMode.HTML,
                )
                await bot.send_message(
                    user_id,
                    "Вы довольны ответом?",
                    reply_markup=get_question_response_buttons_keyboard(0, 0),
                )
                await questionresponse.update_response_admin_id(
                    "question_response",
                    question,
                    message.text,
                    message.from_user.id
                )
                for admin_id in config.ADMIN_IDS:
                    if admin_id != message.from_user.id:
                        await bot.send_message(
                            admin_id,
                            f"Пользователь уже получил ответ на вопрос:\r\n "
                            f"<i>'{question}'</i>!",
                        )
                        await bot.delete_message(admin_id, question_id_in_chat)
            else:
                question = (
                    message.reply_to_message.text.split("'")[1].strip("'")
                )
                user_id = int(
                    message.reply_to_message.text.split(" ")[1].lstrip("(").rstrip(")")
                )
                await bot.send_message(
                    user_id,
                    f"Ответ на вопрос <i>'{question}'</i>:\r\n "
                    f"<b>{message.text}</b>",
                    parse_mode=ParseMode.HTML,
                )
                await bot.send_message(
                    user_id,
                    "Вы довольны ответом?",
                    reply_markup=get_question_response_buttons_keyboard(0, 0),
                )
        except AttributeError:
            await message.answer(
                ("Вы не ответили на сообщение. "
                 "Чтобы отправить пользователю ответ, "
                 "<b>зажмите и удерживайте сообщение с вопросом</b>. "
                 "Далее, после появления меню нажмите <b>'ОТВЕТИТЬ'</b> "
                 "и далее напишите ответ на вопрос пользователя"),
                parse_mode=ParseMode.HTML,
            )


@router.callback_query(
    ContinueStopDialogAction.filter((F.action.in_([
        "continue_dialog",
        "stop_dialog"
    ])))
)
async def continue_stop_dialog(
    call: CallbackQuery,
    callback_data: ContinueStopDialogAction,
    state: FSMContext
):
    """
    Этот хэндлер обрабатывает ответ пользователя
    при желании уточнить ответ админа на его вопрос.
    """
    if callback_data.action == "continue_dialog":
        await call.message.edit_text("Напишите что вы хотели бы уточнить")
        await state.update_data(
            response_admin_id=callback_data.response_admin_id,
            question_id=callback_data.question_id,
        )
        await state.set_state(DialogSteps.start_dialog)
    elif callback_data.action == "stop_dialog":
        await call.message.edit_text("Рады помочь!", reply_markup=None)
        await state.clear()
