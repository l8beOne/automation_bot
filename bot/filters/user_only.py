from aiogram.filters import Filter
from aiogram.types import Message

import config


class IsUserOnlyFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in config.ADMIN_IDS:
            return False
        return True
