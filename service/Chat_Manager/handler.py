from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from service.Registration import isRegister
from service.utils.filter import IsNoTrueDialog
from .utils import service
from ..utils.utils import get_photo_user

manager_chat = Router(name="Chat_Manager")


@manager_chat.message(IsNoTrueDialog(), Command(commands='fantik'))
async def manager(msg: Message, bot: Bot):
    link = await create_start_link(bot, str(msg.chat.id), encode=True)
    markup1 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Перейти в чат",
                url=link,
            )
        ]
    ])
    if await isRegister(msg.from_user.id):
        await msg.answer("Чем могу помочь?", reply_markup=markup1)
    else:
        await msg.answer(text="Давай добавим твоё день рождение в <b>наш</b> календарик", reply_markup=markup1,
                         parse_mode=ParseMode.HTML)


@manager_chat.message(F.new_chat_members)
async def send_welcome(message: Message, bot: Bot):
    link = await create_start_link(bot, str(message.chat.id), encode=True)
    markup1 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Перейти в чат",
                url=link,
            )
        ]
    ])
    bot_obj = await bot.get_me()
    bot_id = bot_obj.id
    for chat_member in message.new_chat_members:
        if chat_member.id == bot_id:

            await bot.send_photo(photo=await get_photo_user(bot=bot, user_id=(await bot.get_me()).id),
                                 chat_id=message.chat.id,
                                 caption="<b>Рад что вы добавили меня, меня зовут Фантик</b>\nЯ напомню всем "
                                         "коллегам о твоём дне и помогу организовать сделать "
                                         f"сбор на твой подарочек, \n\n "
                                         f"<b>Мои супер-способности:</b>\n"
                                         f" ◽️ Показываю все дни рождения чатика\n"
                                         f" ◽️ Помогу придумать поздравление с Днём Рождения\n"
                                         f" ◽️ Создам группу и расскажу всем о твоих желаниях\n\n"
                                         f"<b>Поводов отказываться больше нет, так что нажимай на кнопочку и регистрируйся</b>",
                                 reply_markup=markup1,
                                 parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   reply_markup=markup1,
                                   text=f"<b>@{chat_member.username}, приветствую</b>\n"
                                        f"Заполняй формочку и добавляй свою дату в календарик😇",
                                   parse_mode=ParseMode.HTML)
            await service.add_user_chat(user_id=chat_member.id, chat_id=message.chat.id)


@manager_chat.message(F.left_chat_member)
async def member_left(message: Message, bot: Bot):
    bot_obj = await bot.get_me()
    bot_id = bot_obj.id
    await service.delete_user_chat(chat_id=message.chat.id, user_id=message.left_chat_member.id)
    chat_member = message.left_chat_member
    if chat_member.id == bot_id:
        await service.bot_left_in_chat(chat_id=message.chat.id)
    else:
        await service.delete_user_chat(user_id=chat_member.id, chat_id=message.chat.id)
