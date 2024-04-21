from aiogram.filters import Filter
from aiogram.types import Message
import config


class AdminCommandFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        if message.from_user.id not in config.ADMIN_IDS:    
            return False
        if message.text.split()[0] != self.my_text:
            return False
        return True


class IsAdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id not in config.ADMIN_IDS:    
            return False
        return True
