from aiogram import Bot
from aiogram import types
from aiogram import Dispatcher
from service.birthsday_reg.router import birthday
from config.conifg import BOT_TOKEN


import asyncio
import logging

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)
dp.include_router(birthday)

async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)
    await types.Message.answer("hahahah")


def run():
    asyncio.run(main())
