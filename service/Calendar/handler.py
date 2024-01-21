import aiogram.types.input_file
from aiogram import Router, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton, ChatPhoto,InputMediaPhoto,InputFile
from aiogram.utils.text_decorations import MarkdownDecoration

from service.utils.filter import IsTrueDialog, IsNoTrueDialog
from .filter import IsCalendar, Query
from .utils import service
from .stepform import StepsForm
import aiogram.utils.markdown as md


calendar = Router()

@calendar.message(IsTrueDialog(), IsCalendar())
async def nextBirthday(msg: Message, bot: Bot, state: FSMContext):
    buttons = []
    for i in service.getChatList(msg.from_user.id):
        title = (await bot.get_chat(i)).title
        buttons += [
            InlineKeyboardButton(
                text=title,
                callback_data=str('b' + i)
            )
        ]
    markup1 = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await msg.answer("<b>Так давай посмотрим что у нас тут</b>\n\nВыберите чат для вывода календарика:", reply_markup=markup1, parse_mode=ParseMode.HTML)


@calendar.message(IsNoTrueDialog(), IsCalendar())
async def sendCalendBirthDayToChat(msg: Message, bot:Bot):
    line = service.getseqdate(msg.chat.id)
    await msg.answer(line,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

@calendar.callback_query(Query())
async def sendCalendBirthDay(call: CallbackQuery, bot: Bot):
    data = call.data[1:]
    line = service.getseqdate(data)
    await call.message.answer(text=line, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    await call.answer()
