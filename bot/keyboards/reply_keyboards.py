from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_buttons():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Контакты"))
    builder.row(KeyboardButton(text="Информация Про Вышку"))
    builder.row(KeyboardButton(text="Заказать справку"))
    builder.row(KeyboardButton(text="Узнать расписание"))
    start_keyboard = builder.as_markup(resize_keyboard=True)
    return start_keyboard


def contacts_buttons():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Учебный офис"))
    builder.row(
        KeyboardButton(text="Руководители"),
        KeyboardButton(text="Учителя")
    )
    builder.row(KeyboardButton(text="Назад"))
    contacts_keyboard = builder.as_markup(resize_keyboard=True)
    return contacts_keyboard


def hse_info_buttons():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Гайд по вышке"))
    builder.row(
        KeyboardButton(text="Академический отпуск"),
        KeyboardButton(text="Отчисление")
    )
    builder.row(KeyboardButton(text="Назад"))
    contacts_keyboard = builder.as_markup(resize_keyboard=True)
    return contacts_keyboard
