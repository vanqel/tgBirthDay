from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message
from .service import service


class RegistrationFilter(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        try:
            return msg.text == "Регистрация" or msg.text == "/register"
        except:
            await msg.answer(text="Давай продолжим регистрацию в нашем <b>личном</b> диалоге! ;)")
            return False


class IsRegister(BaseFilter):
    async def __call__(self, msg: Message, bot: Bot) -> bool:
        try:
            if await service.isRegistration(msg.from_user.id):
                return True
        except:
            return False
