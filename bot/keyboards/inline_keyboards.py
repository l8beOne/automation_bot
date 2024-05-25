from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_confirm_button_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить кнопку", callback_data="add_button")
    builder.button(text="Продолжить без кнопки", callback_data="no_button")
    builder.adjust(1)
    confirm_buttons = builder.as_markup()
    return confirm_buttons


class ContinueStopDialogAction(CallbackData, prefix="dialog"):
    action: str
    response_admin_id: int
    question_id: int


def get_question_response_buttons_keyboard(
    response_admin_id: int,
    question_id: int
):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Я не удовлетворен ответом, начать диалог",
        callback_data=ContinueStopDialogAction(
            action="continue_dialog",
            response_admin_id=response_admin_id,
            question_id=question_id,
        ),
    )
    builder.button(
        text="Я удовлетворен ответом",
        callback_data=ContinueStopDialogAction(
            action="stop_dialog", response_admin_id=0, question_id=0
        ),
    )
    builder.adjust(1)
    question_response_buttons = builder.as_markup()
    return question_response_buttons
