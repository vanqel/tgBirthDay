from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class IsCalendar(BaseFilter):
    async def __call__(self, msg: Message) -> True | False:
        return msg.text in ['Календарь', 'Список', "Когда день рождение", '/calendar']


class Query(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> True | False:
        return call.data[0] == 'b'
