from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeChat,
    BotCommandScopeDefault
)

import config


async def set_commands(bot: Bot):
    commands_for_users = [
        BotCommand(
            command="start",
            description="Начало работы",
        ),
        BotCommand(
            command="help",
            description="Правила и рекомендации пользования ботом",
        ),
        BotCommand(
            command="full_name_for_certificate",
            description=("Написать ФИО для получения уведомлений "
                         "о готовности справки"),
        ),
    ]
    commands_for_admins = [
        BotCommand(
            command="start",
            description="Начало работы",
        ),
        BotCommand(
            command="announce",
            description="Начать рассылку",
        ),
        BotCommand(
            command="mute",
            description="Замутить пользователя(запретить писать сообщения)",
        ),
        BotCommand(
            command="full_name_for_certificate",
            description=("Написать ФИО для получения уведомлений "
                         "о готовности справки"),
        ),
    ]
    await bot.set_my_commands(
        commands_for_users,
        scope=BotCommandScopeDefault()
    )
    for admin_id in config.ADMIN_IDS:
        await bot.set_my_commands(
            commands_for_admins, scope=BotCommandScopeChat(chat_id=admin_id)
        )
