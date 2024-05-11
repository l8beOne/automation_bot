from datetime import datetime, timedelta
from aiogram import Router, Bot
from aiogram.types import Message
from utils.response_to_question_class import QuestionResponse
from utils.user_status_class import UserStatusClass
from aiogram.enums import ParseMode
from filters.is_admin_filter import AdminCommandFilter
from apscheduler.schedulers.asyncio import AsyncIOScheduler


router = Router()

@router.message(AdminCommandFilter("/mute"))
async def mute(message: Message, bot: Bot, questionresponse: QuestionResponse, apscheduler: AsyncIOScheduler, userstatus: UserStatusClass):
    '''
    Этот хэндлер будет срабатывать на команду /mute и принимает вместе с ней аргументы: длительность и причина мьюта.
    '''
    if not message.reply_to_message:
         await message.reply("Эта команда должна быть ответом на сообщение!")
         return
    try:
        mute_time_count = int(message.text.split()[1])
        mute_time_type = message.text.split()[2].rstrip(",")
        reason = " ".join(message.text.split()[4:])
    except IndexError:
         await message.answer(f"Для мьюта пользователя введите кол-во времени на которое вы "
                              f"хотите запретить ему писать сообщения в чат с ботом. Также укажите "
                              f"причину мьюта.\nПример сообщения для мьюта:\n/mute 1 день, причина: Спам в бота")
         return
    if mute_time_type in ["минута", "минут", "м", "m", "minutes", "minute"]:
        dt = datetime.now() + timedelta(minutes=mute_time_count)
    elif mute_time_type in ["час", "часов", "ч", "h", "hours", "hour"]:
        dt = datetime.now() + timedelta(hours=mute_time_count)
    elif mute_time_type in ["день", "дней", "д", "d", "days", "day"]:
        dt = datetime.now() + timedelta(days=mute_time_count)
    question = message.reply_to_message.text.split("'")[1].strip("'")
    user_id = await questionresponse.get_user_id_for_reply("question_response", question)
    await userstatus.update_user_status("user_status", user_id, "muted")
    await bot.send_message(user_id, f"Сотрудник учебного офиса запретил вам писать сообщения в бота на время {mute_time_count} {mute_time_type}.\n"
                                    f"Причина: <i>{reason}</i>", parse_mode=ParseMode.HTML)
    apscheduler.add_job(unmute_process, trigger="date", run_date=dt, kwargs={"bot" : bot, "userstatus": userstatus, "user_id" : user_id,})


async def unmute_process(bot: Bot, userstatus: UserStatusClass, user_id: int):
    '''
    Этот хэндлер будет срабатывать через время указанное в аргуменатах к команде /mute.
    '''
    await userstatus.update_user_status("user_status", user_id, "active")
    await bot.send_message(user_id, f"Время мьюта закончилось, вы снова можете писать сообщения в бота")
