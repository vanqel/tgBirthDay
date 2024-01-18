from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from .filter import IsCalendar
from .utils import service
calendar = Router()


@calendar.message(IsCalendar())
async def nextBirthday(msg: Message, bot:Bot):
    await msg.answer("Выберите чат для вывода календарика:")
    for i in service.getChatList(msg.from_user.id):
        print(await bot.get_chat(chat_id=i))