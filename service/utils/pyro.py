from aiogram import Bot
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from database.database import database_manager
from config import *
from service.utils.utils import get_photo_user_bin, logger

app = Client(name="Ассистент BirthdayCSAT", api_id=API_ID, api_hash=API_HASH)


async def main_pyro():
    try:
        await app.start()

    except Exception as e:
        print(f"Произошла ошибка: {e}")


async def createGroup(title, chat_id, target, bot: Bot) -> [str, int]:
        chat = await app.create_supergroup(title=title)
        await chat.set_description(str(chat_id))
        invite_link = await chat.export_invite_link()
        print("CREATE COMPLETE")
        await app.set_chat_photo(chat_id=chat.id, photo=await get_photo_user_bin(target, bot=bot))
        database_manager.set_new_link(user_id=target, chat_id=chat_id, link=invite_link, id_new_chat=str(chat.id))
        await app.send_photo(chat_id=chat.id, photo=await get_photo_user_bin(target, bot=bot),
                             caption="<b>Давайте все вместе придумаем что подарить</b>", parse_mode=ParseMode.HTML)
        about = "<b>"+str(database_manager.get_name(target))+": желает - </b>"+str(database_manager.get_about(target))
        await app.send_message(chat_id=chat.id, text=about, parse_mode=ParseMode.HTML)
        return [str(invite_link), chat.id]

async def printusers():
    for i in [860232046, 721116972, 859417456, 825762787]:
        a = await app.get_users(i)
        print(a.id, a.is_bot)


async def deleteGroup(chat_id):
    await app.delete_supergroup(chat_id=chat_id)
    database_manager.delete_chat_in_user_chat_link(chat_id=chat_id)
    logger(f"{chat_id} - DELETED IN TIME")
