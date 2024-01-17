import datetime
import re

from database.database import manager


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

    async def isRegistration(self, user_id):
        return manager.isRegister(user_id=user_id)

    async def addUser(self, login, user_id, name, date):
        return manager.addUser(login=login, user_id=user_id, name=name, date=date)

    async def deleteUser(self, user_id):
        return manager.deleteuser(user_id)


service = birthday_reg_service()
