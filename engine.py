from aiogram import Bot
from aiogram import types
from aiogram import Dispatcher
from aiogram import F
from aiogram.filters import Command

from service.birthsday_reg.handler import birthday
from config.conifg import BOT_TOKEN

import asyncio
import logging

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)

dp.include_router(birthday)


@dp.message(Command(commands='start'))
async def startMessage(msg: types.Message):
    await msg.answer(
       text= f"Привет, я бот CSAT, который не уедет искать работу в Ростов, \nЯ напомню твоим коллегам нужно сделать сбор на твой подарочек :)")


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


asyncio.run(main())
