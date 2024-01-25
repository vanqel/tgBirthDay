from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message

from database.database import database_manager
from service.Registration import isRegister
from service.utils.filter import IsNoTrueDialog
from .utils import service
from ..utils.pyro import app
from ..utils.utils import logger

manager_chat = Router(name="Chat_Manager")



@manager_chat.message(IsNoTrueDialog(), Command(commands='start'))
async def manager(msg: Message, bot: Bot):

    markup1 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Перейти в чат",
                url="https://t.me/birthdaycsat_bot",
            )
        ]
    ])
    if await isRegister(msg.from_user.id):
        await msg.answer("Чем могу помочь?", reply_markup=markup1)
    else:
        await msg.answer(text="Давай добавим твоё день рождение в <b>наш</b> календарик", reply_markup=markup1,
                         parse_mode=ParseMode.HTML)

@manager_chat.message(IsNoTrueDialog(), Command(commands='restart'))
async def restart_add_link(msg: Message):
    try:
        await app.join_chat(msg.chat.id)
        async for member in app.get_chat_members(chat_id=int(msg.chat.id)):
            if not member.user.is_bot:
                await service.add_user_chat(user_id=member.user.id,chat_id=msg.chat.id)
            logger(f"user_id={member.user.username},chat_id={msg.chat.id}")
    except Exception as ex:
        await msg.answer(text="<b>Возникла ошибка при запуске в вашем чатике</b>\n\n"                
                              "<blockquote>Как только всё будет готово, можете прописать команду /restart</blockquote>",
                         parse_mode=ParseMode.HTML)
        logger(f"call manager_chat {ex}")

@manager_chat.message(F.new_chat_members)
async def send_welcome(message: Message, bot: Bot):
    markup1 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Перейти в чат",
                url="https://t.me/birthdaycsat_bot",
            )
        ]
    ])
    bot_obj = await bot.get_me()
    bot_id = bot_obj.id
    for chat_member in message.new_chat_members:
        if chat_member.id == bot_id:
            await bot.send_message(message.chat.id,
                                   text="<b>Рад что вы добавили меня, меня зовут фантик</b>\nЯ напомню всем "
                                        "коллегам о твоём дне и помогу организовать сделать "
                                        f"сбор на твой подарочек, \n\n "
                                        f"Так что залетайте ко мне в личку, зарегистрируемся :)",
                                   reply_markup=markup1,
                                   parse_mode=ParseMode.HTML)
            try:
                async for member in app.get_chat_members(chat_id=int(message.chat.id)):
                    if not member.user.is_bot:
                        await service.add_user_chat(user_id=member.user.id, chat_id=message.chat.id)
                    logger(f"user_id={member.user.username},chat_id={message.chat.id}")
            except Exception as ex:
                await message.answer(text="<b>Возникла ошибка при запуске в вашем чатике 🙁</b>",
                                 parse_mode=ParseMode.HTML)
                logger(f"call manager_chat {ex}")
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   reply_markup=markup1,
                                   text=f"<b>@{chat_member.username}, приветствую</b>\n"
                                        f"Заполняй формочку и добавляй свою дату в календарик😇")
            await service.add_user_chat(user_id=chat_member.id, chat_id=message.chat.id)

@manager_chat.message(F.left_chat_member)
async def send_welcome(message: Message):
    await service.delete_user_chat(chat_id=message.chat.id, user_id=message.left_chat_member.id)
    await service.delete_chat(chat_id=message.chat.id)


