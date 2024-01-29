from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsTrueDialog(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        try:
            return msg.chat.id == msg.from_user.id
        except:
            return False


class IsNoTrueDialog(BaseFilter):
    # def __init__(self, manager):
    #     self.manager = manager
    async def __call__(self, msg: Message, ) -> bool:
        try:
            #        self.manager.linkUserChat(user_id=msg.from_user.id, chat_id=msg.chat.id )
            return msg.chat.id != msg.from_user.id
        except:
            return False


class IsNoInChatTable(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        try:
            return msg.chat.id != msg.from_user.id
        except:
            return False


class IsAdmin(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        try:
            print(msg.from_user.id == 841244380)
            return msg.from_user.id == "841244380"
        except:
            return False
