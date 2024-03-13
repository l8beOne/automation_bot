from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_confirm_button_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить кнопку", callback_data="add_button")
    builder.button(text="Продолжить без кнопки", callback_data="no_button")
    builder.adjust(1)
    confirm_buttons = builder.as_markup()
    return confirm_buttons
