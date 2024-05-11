import asyncio
from aiogram import Router, Bot, F
from aiogram.types import Message
from utils.database_connect import Request
from utils.response_to_question_class import QuestionResponse
from utils.user_status_class import UserStatusClass
import config
from aiogram.enums import ParseMode
from filters.is_admin_filter import IsAdminFilter

router = Router()

@router.message(F.text.contains("?"))
async def get_question(message: Message, request: Request, questionresponse: QuestionResponse, bot: Bot, userstatus: UserStatusClass):
    '''
    Этот хэндлер получает вопрос пользоваетеля и пересылает его админу в случае, если ответа на этот вопрос еще нет в базе данных.
    '''
    if message.from_user.id not in config.ADMIN_IDS:
        if not await request.check_table("question_response"):
            await request.create_question_response_table("question_response")
        user_status = await userstatus.get_user_status("user_status", message.from_user.id)
        if user_status != "muted":
            if await questionresponse.check_question_in_db("question_response", message.text):
                response = await questionresponse.get_response_from_db("question_response", message.text)
                if response == "Данный вопрос уже находится на рассмотрении у учебного офиса, ожидайте ответа":
                    await message.answer(f"<b>{response}</b>", parse_mode=ParseMode.HTML)
                    await asyncio.sleep(600)
                    return await get_question(message, request, questionresponse, bot)
                else:
                    await message.answer(f"Ответ на вопрос <i>'{message.text}'</i>:\r\n\r\n <b>{response}</b>", parse_mode=ParseMode.HTML)
                    return
            else:
                await message.answer("<i>Я еще не умею отвечать на такой вопрос, зову сотрудника учебного офиса!</i>", parse_mode=ParseMode.HTML)
                await questionresponse.add_question("question_response", message.from_user.id, message.message_id, message.text)
                for admin_id in config.ADMIN_IDS:
                    await bot.send_message(admin_id, f"Пользователь <b>{message.from_user.full_name} ({message.from_user.username})</b> задал вопрос: <i>'{message.text}'</i>", parse_mode=ParseMode.HTML)
        else:
            await message.answer("Вы замьючены и не можете писать сообщения!")
            return

@router.message(IsAdminFilter())
async def get_response_from_admin(message: Message, bot: Bot, questionresponse: QuestionResponse):
    '''
    Этот хэндлер получает ответ от админа на вопрос пользоваетеля и пересылает его пользователю, при этом занося этот ответ в базу данных.
    '''
    if message.text.split()[0] != "/mute":
        try:
            question = message.reply_to_message.text.split("'")[1].strip("'")
            question_id = message.reply_to_message.message_id
            user_id = await questionresponse.get_user_id_for_reply("question_response", question)
            await bot.send_message(user_id, f"Ответ на вопрос <i>'{question}'</i>:\r\n\r\n <b>{message.text}</b>", parse_mode=ParseMode.HTML)
            await questionresponse.update_response("question_response", question,  message.text)
            for admin_id in config.ADMIN_IDS:
                if admin_id != message.from_user.id:
                    await bot.send_message(admin_id, f"Пользователь уже получил ответ на вопрос:\r\n\r\n <i>'{question}'</i>!")
                    await bot.delete_message(admin_id, question_id)
        except AttributeError:
            await message.answer(f"Вы не ответили на сообщение. Чтобы отправить пользователю ответ, "
                                f"<b>зажмите и удерживайте сообщение с вопросом</b>. Далее, после появления меню нажмите <b>'ОТВЕТИТЬ'</b> "
                                f"и далее напишите ответ на вопрос пользователя", parse_mode=ParseMode.HTML)
