from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message


class ManagerChatBase(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        try:
            if msg.text.lower() in ['коробка','календарик', 'когда день рождение?', 'узнать день рождение', '@birthdaycsat_bot']:
                return True
            return False
        except:
            return False
