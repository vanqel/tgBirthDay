import asyncio
import datetime
import logging
import random
from concurrent.futures import ThreadPoolExecutor

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config.config import BOT_TOKEN, birthday_wishes
from database.database import database_manager
from service.Calendar.handler import calendar
from service.Chat_Manager.handler import manager_chat
from service.Registration.handler import birthday
from service.utils.filter import IsTrueDialog, IsNoTrueDialog
from service.utils.pyro import main_pyro, printusers
from service.utils.scheduler import sheduler, loadAllShedulerJob, find_link, test  # , testing  # , test
from service.utils.utils import get_photo_user, logger


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, parse_mode=ParseMode.HTML)

dp.include_router(birthday)
dp.include_router(manager_chat)
dp.include_router(calendar)



@dp.message(Command(commands='test'))
async def test_eng(msg: Message,bot:Bot):
    await test(bot=bot)




@dp.message(Command(commands="gettext"))
async def rand_birth_text(msg:Message):
    await msg.answer(text="<b>Случайное поздравление 🎉</b>\n\n"+
                          random.choice(birthday_wishes)+
                          "\n\n<blockquote>Если хочешь узнать что можно сделать, то отправь /help </blockquote>",
                     parse_mode=ParseMode.HTML)

@dp.message(IsTrueDialog(), Command(commands='start'))
async def startMessage(msg: Message):
    await msg.answer_photo(
        photo=await get_photo_user(6796747094, bot=bot),
        caption=f"<b>Привет, я бот по имени Фантик</b>\n\nЯ <b>не уеду</b> искать работу в Ростов, \n"
                f"Но <b>напомню</b> твоим коллегам, что нужно сделать "
                f"сбор на <b>твой подарочек</b> 😊 \n\n"
                f"<blockquote>Давай начнём регистрацию, отправь мне /register </blockquote>"
                f"<blockquote>Если хочешь узнать что можно сделать, то отправь /help </blockquote>",
        parse_mode=ParseMode.HTML)


@dp.message(IsTrueDialog(), Command(commands='help'))
async def helpMessage(msg: Message):
    await msg.answer("<b>Вот команды которые ты можешь использовать</b>\n\n"
                     "<b>/start</b>              - Запустить и узнать кто же я такой\n"
                     "<b>/calendar</b>      - Узнать ближайшие даты дней рождений\n"
                     "<b>/gettext</b>            - Получить текст случайного поздравления\n"
                     "<b>/register</b>        - Зарегистрироваться в нашей системе\n"
                     "<b>/wishes</b>       - Изменить свой спмсок желаний"
                     "<b>/clearme</b>       - Удалить свои данные\n"
                     "<b>/help</b>               - Узнать список доступных команд\n"
                     , parse_mode=ParseMode.HTML)


@dp.message(IsNoTrueDialog(), Command(commands='help'))
async def helpMessage(msg: Message):
    await msg.answer("<b>Вот команды которые ты можешь использовать</b>\n\n"
                     "<b>/start</b>              - Запустить и узнать кто же я такой\n"
                     "<b>/calendar</b>      - Узнать ближайшие даты дней рождений\n"
                     "<b>/help</b>               - Узнать список доступных команд\n"
                     , parse_mode=ParseMode.HTML)

#['6796747094', '6465682932', '860232046', '697438821']

print
async def main():
    logger.setBot(bot)
    logging.basicConfig(level=logging.INFO)
    await bot.get_updates(False)
    sheduler.start()
    logger(f"---------------------------------------------\n"
           f"<b>BOT START AT {datetime.datetime.now()}</b>")
    await loadAllShedulerJob(bot=bot)
    database_manager.check_connect()
    await dp.start_polling(bot)


if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        asyncio.get_event_loop().run_until_complete(asyncio.gather(main(), main_pyro()))
