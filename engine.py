from aiogram import Bot
from aiogram import types, F
from aiogram import Dispatcher
from aiogram.filters import Command

from service.manager_chat.handler import manager_chat
from service.birthsday_reg.handler import birthday
from service.birthday_base.handler import calendar
from config.conifg import BOT_TOKEN

import asyncio
import logging

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)

dp.include_router(birthday)
dp.include_router(manager_chat)
dp.include_router(calendar)

@dp.message(Command(commands='start'))
async def startMessage(msg: types.Message, bot: Bot):
    await msg.answer(
        text=f"Привет, я бот CSAT, который не уедет искать работу в Ростов, \nЯ напомню твоим коллегам нужно сделать "
             f"сбор на твой подарочек, \n\n Давай начнём регистрацию, отправь мне /register :)")


# https://telegra.ph/Zapusk-funkcij-v-bote-po-tajmeru-11-28
# для напоминаний по дате, важная хуёта, завтра поставить и останется только zoom api и создание чатов

async def main():
    logging.basicConfig(level=logging.DEBUG)
    await bot.get_updates(False)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
