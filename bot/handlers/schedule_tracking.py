import asyncio
from datetime import datetime, timedelta
from typing import List

import aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
from utils.announcement_sender_list import SenderList
from utils.database_connect import Request
from utils.user_status_class import UserStatusClass


async def check_for_updates(params: List):
    """
    Эта функция асинхронно получает данные (значения ячеек) с Google Sheets.
    """
    creds = ServiceAccountCreds(
        **config.SERVICE_ACCOUNT_CREDS,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    async with aiogoogle.Aiogoogle(service_account_creds=creds) as auth:
        sheets_service = await auth.discover("sheets", "v4")
        result = await auth.as_service_account(
            sheets_service.spreadsheets.values.get(
                spreadsheetId=params[0],
                range=params[1],
                majorDimension=params[2]
            )
        )
        values = result.get("values")
        return values


async def compare_prev_current_schedule_results(
    bot: Bot,
    last_data,
    userstatus: UserStatusClass,
    apscheduler: AsyncIOScheduler,
    request: Request,
    senderlist: SenderList,
):
    """
    Этот хендлер сравнивает данные и делает рассылку об изменении в расписании,
    если таковое произошло.
    """
    await asyncio.sleep(600)
    current_data = await check_for_updates(config.SCHEDULE_PARAMS)
    if current_data != last_data:
        if not await request.check_table("schedule_announcement_sender"):
            await request.create_announcement_table(
                "schedule_announcement_sender"
            )
        message_count = await senderlist.transmitter(
            "schedule_announcement_sender", "Расписание изменилось!"
        )
        for admin_id in config.ADMIN_IDS:
            await bot.send_message(
                admin_id,
                f"Уведомление об изменении в расписании отправлено "
                f"{message_count} пользователям!",
            )
        await request.drop_announcement_table("schedule_announcement_sender")
        last_data = current_data
    apscheduler.add_job(
        compare_prev_current_schedule_results,
        trigger="date",
        run_date=datetime.now() + timedelta(milliseconds=1),
        kwargs={
            "bot": bot,
            "last_data": last_data,
            "userstatus": userstatus,
            "apscheduler": apscheduler,
            "request": request,
            "senderlist": senderlist,
        },
    )


async def check_for_status_updates(
    bot: Bot,
    cell_params: List[str],
    user_id: int,
    apscheduler: AsyncIOScheduler
):
    """
    Эта функция отслеживает ячейку статуса справки конкретного пользователя,
    если он заказал справку, но его ячейка со статусом пустая.
    Когда в ячейке со статусом появиться слово 'готово',
    функция уведомит этого пользователя.
    """
    await asyncio.sleep(600)
    current_certificate_status = await check_for_updates(cell_params)
    if (
        current_certificate_status is not None
        and "готово" in current_certificate_status[0][0].lower()
    ):
        await bot.send_message(
            user_id,
            f"Ваша справка готова! Статус: "
            f"'{current_certificate_status[0][0]}'",
        )
        return
    apscheduler.add_job(
        check_for_status_updates,
        trigger="date",
        run_date=datetime.now() + timedelta(milliseconds=1),
        kwargs={
            "bot": bot,
            "cell_params": cell_params,
            "user_id": user_id,
            "apscheduler": apscheduler,
        },
    )


async def check_for_certificate_readiness(
    bot: Bot,
    user_id: int,
    prev_data_user_names: List[List[str]],
    userstatus: UserStatusClass,
    apscheduler: AsyncIOScheduler,
):
    """
    Этот хендлер автоматически уведомляет о готовности справки.
    """
    await asyncio.sleep(600)
    current_data_user_names: List[List[str]] = await check_for_updates(
        config.CERTIFICATE_USER_NAME
    )
    user_full_name = await userstatus.get_user_full_name(
        "user_status",
        user_id
    )
    prev_count_user_name = prev_data_user_names[0].count(user_full_name)
    current_count_user_name = current_data_user_names[0].count(user_full_name)
    if (
        current_data_user_names != prev_data_user_names
        and user_full_name in current_data_user_names[0]
        and current_count_user_name > prev_count_user_name
    ):
        list_of_new_certificate_user_names_indexes = []
        for reversed_index, user_name in enumerate(
            current_data_user_names[0][::-1]
        ):
            if user_name == user_full_name:
                original_index = (
                    len(current_data_user_names[0]) - 1 - reversed_index
                )
                list_of_new_certificate_user_names_indexes.append(
                    original_index
                )
        for i in range(
            current_count_user_name - prev_count_user_name - 1,
            -1,
            -1
        ):
            certificate_status_range = (
                f"Лист1!I{list_of_new_certificate_user_names_indexes[i]+1}"
                f":I{list_of_new_certificate_user_names_indexes[i]+1}"
            )
            user_certificate_status = await check_for_updates([
                config.CERTIFICATE_SPREADSHEET_ID,
                certificate_status_range,
                "ROWS"
            ])
            if user_certificate_status is None:
                await check_for_status_updates(
                    bot,
                    [
                        config.CERTIFICATE_SPREADSHEET_ID,
                        certificate_status_range,
                        "ROWS",
                    ],
                    user_id,
                    apscheduler,
                )
            else:
                certificate_status = user_certificate_status[0][0]
                if "готово" in certificate_status.lower():
                    await bot.send_message(
                        user_id,
                        f"Ваша справка готова! Статус: "
                        f"'{user_certificate_status}'",
                    )
        prev_data_user_names = current_data_user_names
    apscheduler.add_job(
        check_for_certificate_readiness,
        trigger="date",
        run_date=datetime.now() + timedelta(milliseconds=1),
        kwargs={
            "bot": bot,
            "user_id": user_id,
            "prev_data_user_names": prev_data_user_names,
            "userstatus": userstatus,
            "apscheduler": apscheduler,
        },
    )
