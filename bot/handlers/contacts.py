import keyboards
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message


router = Router()

NAME_USERNAME = { 
    "учебный офис": {
        "<b>Нестерова Татьяна Валерьевна</b>: " : "@Tatyana_Nesterowa, ",
        "<b>Звидрина Анна Михайловна</b>: " : "@anzvi",
        "<b>Ксения Алексеевна</b>: " : "@ksuumii",
        "<b>Харькова Анастасия Вадимовна</b>: " : "@aakharkovaa",
    },
    "руководители": {
        "<b>Антон Кузнецов - Замдекана</b>: " : "@kuzik566",
        "<b>Кольцов Сергей Николаевич - Академический руководитель ПАДИИ</b>: " : "@",
        "<b>Храбров Александр Игоревич - Академический руководитель ПМИ</b>: " : "@",
        "<b>Мухин Михаил Сергеевич - Декан</b>: " : "@MikeMukhin",
    },
    "учителя": {
        "<b>Тут есть все учителя и их контакты</b>: " : "https://spb.hse.ru/ba/dataanalytics/tutors"
    }
}


@router.message(F.text.lower() == "контакты")
async def conacts_commands(message: Message):
    '''
    Этот хэндлер обрабатывает кнопку "Контакты".
    '''
    await message.answer(
        text = "Здесь вы можете получить все контакты",
        reply_markup= await keyboards.contacts_buttons()
    )


@router.message(F.text.lower() == "учебный офис")
@router.message(F.text.lower() == "руководители")
@router.message(F.text.lower() == "учителя")
async def process_contacts_commands(message: Message):
    '''
    Этот хэндлер обрабатывает кнопки контактов.
    '''
    for item, contact_dict in NAME_USERNAME.items():
        if message.text.lower() == item:
            content = "".join([f"{username}\n <a>{contacts}</a>\n" for username, contacts in contact_dict.items()])
            await message.answer(
                text = content,
                parse_mode=ParseMode.HTML,
                reply_markup= await keyboards.contacts_buttons()
            )
