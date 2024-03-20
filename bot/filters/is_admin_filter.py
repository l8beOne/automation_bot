from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message
import config
from aiogram.filters import CommandObject

#router = Router()


class IsAdminFilter(Filter):
    def __init__(self, command: str, admin_id: int) -> None:
        self.admin_id = admin_id
        self.command = command

    async def __call__(self, message: Message) -> bool:
        message_text = message.text.strip()
        message_words = message_text.split(" ")
        if message.from_user.id == self.admin_id:
            print(self.admin_id)
            if message_words[0].startswith("/") and message_words[0][1:] == self.command:
                print(message_text)
                return True
        #return (message.from_user.id == self.admin_id and (message_words[0].startswith("/") and message_words[0][1:] == self.command))
