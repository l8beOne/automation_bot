from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_buttons():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Контакты")
    )
    builder.row(
        KeyboardButton(text="Информация Про Вышку")
    )
    builder.row(
        KeyboardButton(text="Узнать расписание")
    )
    start_keyboard = builder.as_markup(resize_keyboard=True)
    return start_keyboard


def contacts_buttons():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Учебный офис")
    )
    builder.row(
        KeyboardButton(text="Руководители"),
        KeyboardButton(text="Учителя")
    )
    builder.row(
        KeyboardButton(text="Назад")
    )
    contacts_keyboard = builder.as_markup(resize_keyboard=True)
    return contacts_keyboard


def hse_info_buttons():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Гайд по вышке")
    )
    builder.row(
        KeyboardButton(text="Академический отпуск"),
        KeyboardButton(text="Отчисление")
    )
    builder.row(
        KeyboardButton(text="Назад")
    )
    contacts_keyboard = builder.as_markup(resize_keyboard=True)
    return contacts_keyboard


def schedule_op_course_buttons():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="ПАДИИ 1"),
        KeyboardButton(text="ПМИ 1")
    )
    builder.row(
        KeyboardButton(text="ПАДИИ 2"),
        KeyboardButton(text="ПМИ 2")
    )
    op_course_keyboard = builder.as_markup(resize_keyboard=True)
    return op_course_keyboard


def schedule_day_buttons():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="ПН"),
        KeyboardButton(text="ВТ"),
        KeyboardButton(text="СР"),
        KeyboardButton(text="ЧТ"),
        KeyboardButton(text="ПТ"),
        KeyboardButton(text="СБ")
    )
    builder.row(
        KeyboardButton(text="Назад")
    )
    day_selection_keyboard = builder.as_markup(resize_keyboard=True)
    return day_selection_keyboard
