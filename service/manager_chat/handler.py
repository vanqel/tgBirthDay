from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from service.utils.filter import IsTrueDialog, IsNoTrueDialog
from service.birthsday_reg import isRegister
from .filter import ManagerChatBase
from .utils import service
from .stepform import StepsForm

manager_chat = Router(name="manager_chat")


@manager_chat.message(IsNoTrueDialog(), ManagerChatBase())
async def manager(msg: Message,bot: Bot):
    if await isRegister(msg.from_user.id):
        markup1 = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Перейти в чат",
                    url="https://t.me/birthdaycsat_bot",
                )
            ]
        ])
        await msg.answer("Список доступных комманд",reply_markup=markup1)
    else:
        markup2 = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Перейти в чат",
                    url="https://t.me/birthdaycsat_bot",
                )
            ]
        ])
        await msg.answer(text="Давай добавим твоё день рождение в наш календарик", reply_markup=markup2)


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
            await bot.send_message(message.chat.id,text="Я родился \nСпасибо что добавил меня, о Великий Админ группы \nЯ напомню всем коллегам о твоём дне и помогу организовать сделать "
             f"сбор на твой подарочек, \n\n Так что залетайте ко мне в личку, зарегистрируемся :)",reply_markup=markup1)
        else:
            await service.add_user_chat(user_id=chat_member.id, chat_id=message.chat.id)

@manager_chat.message(F.left_chat_member)
async def send_welcome(message: Message):
    await service.delete_user_chat(chat_id=message.chat.id,user_id=message.left_chat_member.id)