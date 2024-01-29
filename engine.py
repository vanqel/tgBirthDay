import asyncio
import datetime
import logging
import random
from concurrent.futures import ThreadPoolExecutor

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.payload import decode_payload

from config.config import BOT_TOKEN, birthday_wishes
from database.database import database_manager
from service.Calendar.handler import calendar
from service.Chat_Manager.handler import manager_chat
from service.Chat_Manager.utils import service
from service.Registration.handler import birthday
from service.utils.filter import IsTrueDialog, IsNoTrueDialog, IsAdmin
from service.utils.pyro import main_pyro
from service.utils.scheduler import sheduler, loadAllShedulerJob, test
from service.utils.utils import get_photo_user, logger

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, parse_mode=ParseMode.HTML)

dp.include_router(birthday)
dp.include_router(manager_chat)
dp.include_router(calendar)


@dp.message(Command(commands='teresteted'))
async def test_eng(msg: Message, bot: Bot):
    await test(bot=bot)


@dp.message(Command(commands="gettext"))
async def rand_birth_text(msg: Message):
    await msg.answer(text="<b>Случайное поздравление 🎉</b>\n\n" +
                          random.choice(birthday_wishes) +
                          "\n\n<blockquote>Если хочешь узнать что можно сделать, то отправь /help </blockquote>",
                     parse_mode=ParseMode.HTML)


@dp.message(IsTrueDialog(), Command(commands='start'))
async def startMessage(msg: Message, command: Command = None):
    if command.args is not None:
        args = command.args
        reference = decode_payload(args)
        await service.add_user_chat(user_id=msg.from_user.id, chat_id=reference)
        await msg.answer_photo(
            photo=await get_photo_user(user_id=(await bot.get_me()).id, bot=bot),
            caption=f"<b>Привет, я бот по имени Фантик</b>\n\nЯ <b>не уеду</b> искать работу в Ростов, \n"
                    f"Но <b>напомню</b> твоим коллегам, что нужно сделать "
                    f"сбор на <b>твой подарочек</b> 😊 \n\n"
                    f"<blockquote>Давай начнём регистрацию, отправь мне /register </blockquote>"
                    f"<blockquote>Если хочешь узнать что можно сделать, то отправь /help </blockquote>",
            parse_mode=ParseMode.HTML)
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выбери чатик",
                                     url=f"tg://resolve?domain={(await bot.get_me()).username}&startgroup=true")
            ]
        ])
        await msg.answer_photo(
            photo=await get_photo_user((await bot.get_me()).id, bot=bot),
            caption=f"<b>Привет, я бот по имени Фантик</b>\n\nЯ <b>не уеду</b> искать работу в Ростов, \n"
                    f"Но <b>напомню</b> твоим коллегам, что нужно сделать "
                    f"сбор на <b>твой подарочек</b> 😊 \n\n"
                    f"Я работаю с группами, поэтому нажми на кнопочку снизу и добавь меня в свой чатик",
            parse_mode=ParseMode.HTML,
            reply_markup=markup)


@dp.message(IsTrueDialog(), Command(commands='help'))
async def helpMessage(msg: Message):
    await msg.answer("<b>Вот команды которые ты можешь использовать</b>\n\n"
                     "<b>/start</b>              - Запустить и узнать кто же я такой\n"
                     "<b>/calendar</b>      - Узнать ближайшие даты дней рождений\n"
                     "<b>/gettext</b>            - Получить текст случайного поздравления\n"
                     "<b>/register</b>        - Зарегистрироваться в нашей системе\n"
                     "<b>/wishes</b>       - Изменить свой спмсок желаний\n"
                     "<b>/clearme</b>       - Удалить свои данные\n"
                     "<b>/help</b>               - Узнать список доступных команд\n"
                     , parse_mode=ParseMode.HTML)


@dp.message(IsNoTrueDialog(), Command(commands='help'))
async def helpMessage(msg: Message):
    await msg.answer("<b>Вот команды которые ты можешь использовать</b>\n\n"
                     "<b>/start</b>              - Запустить и узнать кто же я такой\n"
                     "<b>/calendar</b>      - Узнать ближайшие даты дней рождений\n"
                     "<b>/fantik</b>       - Узнать ближайшие даты дней рождений\n"
                     "<b>/help</b>               - Узнать список доступных команд\n"
                     , parse_mode=ParseMode.HTML)

@dp.message(IsAdmin(),Command(commands='setuniccode'))
async def setcode(msg:Message):
    a = msg.text
    a = a.split(".",1)
    await msg.answer(a[0]+"___"+a[1])
async def main():
    logger.setBot(bot)
    logging.basicConfig(level=logging.INFO)
    sheduler.start()
    logger(f"---------------------------------------------\n"
           f"<b>BOT START AT {datetime.datetime.now()}</b>")
    await loadAllShedulerJob(bot=bot)
    database_manager.check_connect()
    await dp.start_polling(bot)


if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        asyncio.get_event_loop().run_until_complete(asyncio.gather(main(), main_pyro()))
