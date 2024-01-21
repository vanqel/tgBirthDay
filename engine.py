import datetime

from aiogram import Bot
from aiogram import types, F
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from service.utils.filter import IsTrueDialog, IsNoTrueDialog
from service.utils.utils import get_photo_user, logger
from service.Chat_Manager.handler import manager_chat
from service.Registration.handler import birthday
from service.Calendar.handler import calendar
from config.config import BOT_TOKEN
from service.utils.scheduler import sheduler, loadAllShedulerJob

import asyncio
import logging


# Создаем асинхронный обработчик логов


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, parse_mode=ParseMode.HTML)

dp.include_router(birthday)
dp.include_router(manager_chat)
dp.include_router(calendar)




@dp.message(IsTrueDialog(), Command(commands='start'))
async def startMessage(msg: Message):
    await msg.answer_photo(
        photo=await get_photo_user(6796747094, bot=bot),
        caption=f"<b>Привет, я бот CSAT</b>\n\nЯ <b>не уеду</b> искать работу в Ростов, \n"
                f"Но <b>напомню</b> твоим коллегам, что нужно сделать "
                f"сбор на <b>твой подарочек</b> 😊 \n\n"
                f"<blockquote>Давай начнём регистрацию, отправь мне /register </blockquote>"
                f"<blockquote>Если хочешь узнать что можно сделать, то отправь /help </blockquote>",
        parse_mode=ParseMode.HTML)

@dp.message(Command(commands='help'))
async def helpMessage(msg: Message):
    await msg.answer("<b>Вот команды которые ты можешь использовать</b>\n\n"
                     "<b>/start</b>              - Запустить и узнать кто же я такой\n"
                     "<b>/calendar</b>      - Узнать ближайшие даты дней рождений\n"
                     "<b>/register</b>        - Зарегистрироваться в нашей системе\n"
                     "<b>/clearme</b>       - Удалить свои данные\n"
                     "<b>/help</b>               - Узнать список доступных команд\n"
                     , parse_mode=ParseMode.HTML)
# https://telegra.ph/Zapusk-funkcij-v-bote-po-tajmeru-11-28
# для напоминаний по дате, важная штука, завтра поставить и останется только zoom api и создание чатов

async def main():
    logger.setBot(bot)
    logging.basicConfig(level=logging.INFO)
    await bot.get_updates(False)
    sheduler.start()

    logger(f"---------------------------------------------\n"
        f"<b>BOT START AT {datetime.datetime.now()}</b>")
    await loadAllShedulerJob(bot=bot)
    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())
