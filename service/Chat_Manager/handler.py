from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message
from aiogram.filters import Command
from service.Registration import isRegister
from service.utils.filter import IsNoTrueDialog
from .filter import ManagerChatBase
from .utils import service

manager_chat = Router(name="Chat_Manager")


@manager_chat.message(IsNoTrueDialog(), Command(commands='start'))
async def manager(msg: Message):
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
        await msg.answer(text="Давай добавим твоё день рождение в <b>наш</b> календарик", reply_markup=markup1, parse_mode=ParseMode.HTML)
    await service.add_user_chat(user_id=msg.from_user.id, chat_id=msg.chat.id)
    await service.add_chat(msg.chat.id)


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
            await service.add_chat(message.chat.id)
            await bot.send_message(message.chat.id,
                                   text="Я родился \nСпасибо что добавил меня, о Великий Админ группы \nЯ напомню всем "
                                        "коллегам о твоём дне и помогу организовать сделать "
                                        f"сбор на твой подарочек, \n\n "
                                        f"Так что залетайте ко мне в личку, зарегистрируемся :)",
                                   reply_markup=markup1)
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   reply_markup=markup1,
                                   text=f"Приветики, @{message.from_user.username} "
                                        f"заполняй формочку и добавляй свою дату ;)")
            await service.add_user_chat(user_id=chat_member.id, chat_id=message.chat.id)


@manager_chat.message(F.left_chat_member)
async def send_welcome(message: Message):
    await service.delete_user_chat(chat_id=message.chat.id, user_id=message.left_chat_member.id)
