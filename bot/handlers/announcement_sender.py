from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from filters.is_admin_filter import AdminCommandFilter
from keyboards import inline_keyboards
from utils.announcement_sender_list import SenderList
from utils.database_connect import Request
from utils.states import AnnouncementSteps

router = Router()


@router.message(AdminCommandFilter("/announce"))
async def make_announce(message: Message, state: FSMContext):
    """
    Этот хэндлер обрабатывает комманду "announce" и
    переводит пользователя в состояние отправки текста для объявления.
    """
    args = " ".join(message.text.split()[1:])
    if not args:
        await message.answer(
            "Для создания рассылки введите комманду /announce и имя рассылки "
        )
        return
    await message.answer(
        f"Приступаем создавать рассылку. Имя объявления - {args}\r\n\r\n"
        f"Отправьте сообщение, которое будет использовано как объявление"
    )
    await state.update_data(announce_name=args)
    await state.set_state(AnnouncementSteps.get_announcement_message)


@router.message(AnnouncementSteps.get_announcement_message)
async def get_announcement_message(message: Message, state: FSMContext):
    """
    Этот хэндлер обрабатывает текст объявления
    и предлагает добавть кнопку в него.
    """
    await message.answer(
        "Я запомнил сообщение, которое вы хотите разослать.\r\n"
        "Хотите добавить кнопку для ссылки?",
        reply_markup=inline_keyboards.get_confirm_button_keyboard(),
    )
    await state.update_data(
        message_text=message.text,
        message_id=message.message_id,
        chat_id=message.from_user.id,
    )
    await state.set_state(AnnouncementSteps.select_button)


@router.callback_query(AnnouncementSteps.select_button)
async def select_button(call: CallbackQuery, bot: Bot, state: FSMContext):
    """
    Этот хэндлер обрабатывает добавление кнопки/продолжение без кнопки.
    """
    if call.data == "add_button":
        await call.message.answer(
            "Отправьте текст для кнопки.",
            reply_markup=None
        )
        await state.set_state(AnnouncementSteps.get_text_button)
    elif call.data == "no_button":
        await call.message.edit_reply_markup(reply_markup=None)
        data = await state.get_data()
        message_text = data.get("message_text")
        message_id = int(data.get("message_id"))
        chat_id = int(data.get("chat_id"))
        await confirm(call.message, bot, message_text, message_id, chat_id)
        await state.set_state(AnnouncementSteps.get_url)
    await call.answer()


@router.message(AnnouncementSteps.get_text_button)
async def get_text_button(message: Message, state: FSMContext):
    """
    Этот хэндлер обрабатывает текст для кнопки.
    """
    await state.update_data(button_text=message.text)
    await message.answer("Отправьте ссылку для кнопки!")
    await state.set_state(AnnouncementSteps.get_url)


@router.message(AnnouncementSteps.get_url)
async def get_url(message: Message, bot: Bot, state: FSMContext):
    """
    Этот хэндлер обрабатывает ссылку для кнопки.
    """
    await state.update_data(button_url=message.text)
    added_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=(await state.get_data()).get("button_text"),
                    url=f"{message.text}",
                )
            ]
        ]
    )
    data = await state.get_data()
    message_text = data.get("message_text")
    message_id = int(data.get("message_id"))
    chat_id = int(data.get("chat_id"))
    await confirm(
        message, bot, message_text, message_id, chat_id, added_keyboard
    )


async def confirm(
    message: Message,
    bot: Bot,
    message_text: str,
    message_id: int,
    chat_id: int,
    reply_markup: InlineKeyboardMarkup = None,
):
    """
    Этот хэндлер обрабатывает подтверждение/отмену сформированного объявления.
    """
    await bot.copy_message(
        chat_id, chat_id, message_id, reply_markup=reply_markup
    )
    await message.answer(
        ("Вот объявление, которое будет отправлено. "
         "Подтвердите или отмените его."),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Подтвердить", callback_data="confirm_announce"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Отменить", callback_data="cancel_announce"
                    )
                ],
            ]
        ),
    )


@router.callback_query(F.data.in_(["confirm_announce", "cancel_announce"]))
async def send_process(
    call: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    request: Request,
    senderlist: SenderList,
):
    """
    Этот хэндлер обрабатывает процесс отправки рассылки(объявления).
    """
    data = await state.get_data()
    message_text = data.get("message_text")
    message_id = data.get("message_id")
    chat_id = data.get("chat_id")
    button_text = data.get("button_text")
    button_url = data.get("button_url")
    announce_name = data.get("announce_name")
    if call.data == "confirm_announce":
        await call.message.edit_text("Начинаю рассылку!", reply_markup=None)
        if not await request.check_table(announce_name):
            await request.create_announcement_table(announce_name)
        message_count = await senderlist.transmitter(
            announce_name, message_text, message_id,
            chat_id, button_text, button_url
        )
        await call.message.answer(
            f"Объявление успешно отправлено {message_count} пользователям!"
        )
        await request.drop_announcement_table(announce_name)
    elif call.data == "cancel_announce":
        await call.message.edit_text("Отменил рассылку", reply_markup=None)
    await state.clear()
