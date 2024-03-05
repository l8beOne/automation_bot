import keyboards
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message


router = Router()

BUTTON_INFO = {
    "гайд по вышке" : f"Этот гайд введет вас в учебеную жизнь и немного расскажет о вышке в целом:\n ⬇️⬇️⬇️ \n"
                      f"https://hsefirsttime.notion.site/a7d19f352a604bcd8d57c8f0816fc28e?v=03f6aadb0adf4054a40b2f1ae3eebd8f",
    "академический отпуск" : f"<b>-Основания и порядок предоставления академического отпуска. Допуск к занятиям после выхода из академического отпуска\n\n"
                             f"-Кто принимает решение о предоставлении академического отпуска?\n\n"
                             f"-Могут ли мне отказать в предоставлении академического отпуска?\n\n"
                             f"-Включается ли период нахождения в академическом отпуске в срок освоения образовательной программы?\n\n"
                             f"-На каких основаниях может быть предоставлен академический отпуск?\n\n"
                             f"-Как получить академический отпуск в целях создания университетского стартапа?\n\n"
                             f"-Могу ли я взять академический отпуск с целью обучения в иностранном университете?\n\n"
                             f"-Каков порядок действий при выходе из академического отпуска?\n\n"
                             f"-Сохраняется ли бюджетное место за студентом, обучавшимся на бюджете?</b>\n\n"
                             f"Все это вы можете узнать здесь:\n ⬇️⬇️⬇️ \n"
                             f"https://www.hse.ru/studyspravka/academotpusk/",
    "отчисление" : f"<b>-В каких случаях студент может быть отчислен из Высшей школы экономики?\n\n"
                   f"-Что такое добросовестное освоение образовательной программы?\n\n"
                   f"-Может ли студент быть отчислен во время болезни, академического отпуска, отпуска по беременности и родам, "
                   f"отпуска по уходу за ребёнком до достижения им возраста 3-х лет?\n\n"
                   f"-Документы</b>\n\n"
                   f"Вся информация доступна здесь:\n ⬇️⬇️⬇️ \n"
                   f"https://www.hse.ru/studyspravka/otch/"
}

@router.message(F.text.lower() == "информация про вышку")
async def hse_info_commands(message: Message):
    '''
    Этот хэндлер обрабатывает кнопку "Информация про вышку".
    '''
    await message.answer(
        text = "Здесь вы можете получить информацию и гайд по Вышке",
        reply_markup= await keyboards.hse_info_buttons()
    )


@router.message(F.text.lower() == "гайд по вышке")
@router.message(F.text.lower() == "академический отпуск")
@router.message(F.text.lower() == "отчисление")
async def process_contacts_commands(message: Message):
    '''
    Этот хэндлер обрабатывает кнопки инорфмации о вышке.
    '''
    for item, text in BUTTON_INFO.items():
        if message.text.lower() == item:
            await message.answer(
                text = text,
                parse_mode=ParseMode.HTML,
                reply_markup= await keyboards.hse_info_buttons()
            )
