from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsCalendar(BaseFilter):
    async def __call__(self, msg:Message) -> True | False:
        return msg.text in ['Календарь', 'Список', "Когда день рождение",'/calendar']