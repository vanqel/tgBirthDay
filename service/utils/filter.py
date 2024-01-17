from aiogram.filters import BaseFilter
from aiogram.types import Message
class IsTrueDialog(BaseFilter):
    async def __call__(self, msg : Message) -> bool:
        try:
            return msg.chat.id == msg.from_user.id
        except:
            return False
