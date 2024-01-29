import datetime
import re

from pyrogram.enums import ParseMode

from database.database import database_manager
from ..utils.pyro import app
from ..utils.scheduler import sheduler
from ..utils.utils import logger


class birthday_reg_service:
    def validate_date(self, date):
        date_regex = re.compile(r'^\d{2}-\d{2}-\d{4}$')
        if date_regex.match(date):
            if int(date[6:10]) > 2024: return [False, None]
            if int(date[4:5]) > 12: return [False, None]
            if int(date[0:2]) > 31: return [False, None]
            try:
                date_obj = datetime.date(year=int(date[6:10]), month=int(date[4:5]), day=int(date[0:2]))
                return [True, date_obj]
            except:
                return [False, None]
        else:
            return [False, None]

    async def send_new_about(self, user_id, about):
        try:
            name = database_manager.get_name(user_id)
            list_cid = database_manager.get_all_new_link(user_id=user_id)
            for cid in list_cid:
                await app.send_message(chat_id=cid,
                                       text=f"<b>У пользователя - {name}, обновился список желаний\n</b> {about}",
                                       parse_mode=ParseMode.HTML)
        except:
            pass

    async def isRegistration(self, user_id):
        return database_manager.is_registered(user_id=user_id)

    async def add_user(self, login, user_id, name, date):
        return database_manager.add_user(login=login, user_id=user_id, name=name, date=date)

    async def deleteUser(self, user_id):
        list_job = sheduler.get_jobs()
        for i in list_job:
            if i.name == user_id:
                sheduler.remove_job(job_id=i.id)
        logger(f"DELETE: <b> JOB FOR USER_ID - {i.name}</b>")
        return database_manager.delete_user(user_id)


service = birthday_reg_service()
