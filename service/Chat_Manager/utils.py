from aiogram import Bot
from aiogram.enums import ChatMemberStatus

from database.database import database_manager
from service.utils.scheduler import sheduler


class ManagerChatUtils:
    def __init__(self):
        pass

    async def add_chat(self, chat_id):
        database_manager.add_chat(chat_id=chat_id)

    async def get_link_chat(self, user_id, bot: Bot):
        for chat_id in database_manager.get_all_chats():
            try:
                chat_members = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
                if chat_members.status != ChatMemberStatus.LEFT:
                    database_manager.link_user_chat(user_id=user_id, chat_id=chat_id)
            except Exception as ex:
                print(ex)

    async def add_user_chat(self, user_id, chat_id):
        database_manager.link_user_chat(user_id=user_id, chat_id=chat_id)

    async def delete_user_chat(self, user_id, chat_id):
        database_manager.delete_user_in_chat(user_id=user_id, chat_id=chat_id)

    async def delete_chat(self, chat_id):
        database_manager.delete_chat(chat_id=chat_id)

    async def bot_left_in_chat(self, chat_id):
        database_manager.clearchat(chat_id)
        a = sheduler.get_jobs()
        for i in a:
            name_job = i.name
            uid, cid, date = name_job.split('.')
            if cid == chat_id:
                sheduler.remove_job(name_job)


service = ManagerChatUtils()
