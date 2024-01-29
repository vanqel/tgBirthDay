import datetime
import random

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import birthday_wishes
from database.database import database_manager
from .pyro import createGroup, deleteGroup_chat_id, deleteGroup_target
from .utils import logger, get_photo_user

sheduler = AsyncIOScheduler(timezone='Europe/Moscow', executor="asyncio")


async def find_link(target_user, chat_id, chat_title, bot) -> {'title': str,
                                                               'new_chat_id': int,
                                                               'url': str}:
    link_in_db = database_manager.get_new_link(user_id=target_user, chat_id=chat_id)
    name = database_manager.get_name(target_user)
    title = f"ДР {name} | {chat_title}"
    print(link_in_db)
    if link_in_db is None:
        new_link, new_chat_id = await createGroup(title, bot=bot, chat_id=int(chat_id),
                                                  target=int(target_user))
        return {'title': title, 'new_chat_id': new_chat_id, 'url': new_link}
    else:
        return {'title': title, 'new_chat_id': link_in_db[1], 'url': link_in_db[0]}


async def loadAllShedulerJob(bot: Bot):
    logger("SHEDULER START ADDING JOB")

    async def job():
        users = database_manager.get_all_users()
        dates_delete = database_manager.get_all_link_dates()
        sheduler.remove_all_jobs()
        try:
            if users is not None:
                for target in users:
                    await sendDayInChat(bot, target[1])
            if dates_delete is not None:
                for date in dates_delete:
                    await deleting(date[0], date[1])
            logger("INFO: <b> ALL SCHEDULER JOBS COMPLETE</b>")
        except Exception as ex:
            logger(f"ERROR: SCHEDULER <b>{ex}</b>")

    #
    await job()
    sheduler.add_job(job, trigger='interval', hours=12)


async def deleting(chat_id, date):
    id_new_chat = chat_id

    async def delete(id_new_chat):
        await deleteGroup_chat_id(id_new_chat)

    sheduler.add_job(delete, 'date', run_date=date, args=[chat_id])


async def bot_send_message(bot: Bot, chat_id, target):
    name = database_manager.get_name(target)
    await bot.send_photo(chat_id=chat_id,
                         photo=await get_photo_user(target, bot=bot),
                         caption=f"<b>{name}</b>   🎉\n{random.choice(birthday_wishes)}",
                         parse_mode=ParseMode.HTML)


async def send_update_wishes(bot: Bot, target):
    await bot.send_message(chat_id=target, text="<b>У кого то скоро день рождение</b>\n\n"
                                                "Советую перепроверить свой виш лист\n"
                                                "<blockquote>Обновить виш лист можно командой - /wishes</blockquote>",
                           parse_mode=ParseMode.HTML)


async def sendMessageTarget(bot: Bot, chat_id, target_user, caption):
    name = database_manager.get_name(target_user)
    chat = await bot.get_chat(chat_id=str(chat_id))
    chat_title = chat.title
    dict_data = await find_link(target_user=target_user, bot=bot, chat_id=chat_id, chat_title=chat_title)
    markup12 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=str(name + " | " + chat_title),
                url=dict_data['url']
            )
        ]
    ])
    for user in database_manager.get_list_users_target_birthdays(chat_id=chat_id, target=target_user):
        try:
            await bot.send_photo(caption=caption.format(name),
                                 chat_id=user,
                                 photo=await get_photo_user(user_id=target_user, bot=bot),
                                 reply_markup=markup12)
        except Exception as ex:
            print(ex)


def setDateCreate(date: datetime.date, type_date: int = 1, delta_days: int = 0):
    """
    Определяет новую дату для задачи
    :param delta_days:
    :param date:
    :param type_date:

    type 1: new date create\n
    type 2: convert datetime.date -> datetime.datetime\n
    type 3: timedelta
    """
    if date is None:
        return datetime.datetime.now()
    date = datetime.datetime(day=date.day, month=date.month, year=date.year)
    match type_date:
        case 1:
            if 1 <= date.day <= 10:
                if date.month - 1 > 0:
                    date = date.replace(day=25, month=date.month - 1)
                else:
                    date = date.replace(day=25, month=12, year=date.year - 1)
                if date < datetime.datetime.now():
                    return datetime.datetime.now().replace(hour=12, minute=30)
                return datetime.datetime(day=date.day, month=date.month, year=date.year, hour=12, minute=30)
            elif 10 < date.day <= 25:
                if date.month - 1 > 0:
                    date = date.replace(day=25, month=date.month - 1)
                else:
                    date = date.replace(day=25, month=12, year=date.year - 1)
                if date < datetime.datetime.now():
                    return datetime.datetime.now().replace(hour=12, minute=30)
                return datetime.datetime(day=date.day, month=date.month, year=date.year, hour=12, minute=30)
            elif 25 < date.day <= 31:
                print(f"DATE NEW V3- {date}")
                date = date.replace(day=10)
                if date < datetime.datetime.now():
                    return datetime.datetime.now().replace(hour=12, minute=30)
            return datetime.datetime(day=date.day, month=date.month, year=date.year, hour=12, minute=30)
        case 2:
            return datetime.datetime(day=date.day, month=date.month, year=date.year, hour=12, minute=30)
        case 3:
            return datetime.datetime(day=date.day, month=date.month, year=date.year, hour=12, minute=30) - \
                datetime.timedelta(days=delta_days)


async def sendDayInChat(bot: Bot, target_user):
    chats = database_manager.get_user_in_chat(target_user)
    for chat_id in chats:
        date = database_manager.get_target_birthdays(target=target_user)
        datetime_birth = date
        caption_start = "Скоро {} празднует день рождение. Самое время начинать думать над подарочком"
        caption_5 = "Через 5 дней, {} празднует день рождение. Самое время начинать готовить поздравление!"
        caption_1 = "Уже завтра, {} празднует день рождение"
        caption_now = "Сегодня {} празднует день рождение!"
        sheduler.add_job(sendMessageTarget,
                         trigger='date',
                         next_run_time=setDateCreate(datetime_birth, 1),
                         name=str(target_user) + "." + str(chat_id) + "." + str(setDateCreate(datetime_birth, 1)),
                         args=[bot, chat_id, target_user, caption_start])
        sheduler.add_job(sendMessageTarget,
                         trigger='date',
                         next_run_time=setDateCreate(datetime_birth, 3, 5),
                         name=str(target_user) + "." + str(chat_id) + "." + str(datetime_birth),
                         args=[bot, chat_id, target_user, caption_5])
        sheduler.add_job(sendMessageTarget,
                         trigger='date',
                         next_run_time=setDateCreate(datetime_birth, 3, 1),
                         name=str(target_user) + "." + str(chat_id) + "." + str(datetime_birth),
                         args=[bot, chat_id, target_user, caption_1])
        sheduler.add_job(sendMessageTarget,
                         trigger='date',
                         next_run_time=setDateCreate(datetime_birth, 2),
                         name=str(target_user) + "." + str(chat_id) + "." + str(datetime_birth),
                         args=[bot, chat_id, target_user, caption_now])
        sheduler.add_job(bot_send_message,
                         trigger='date',
                         next_run_time=setDateCreate(datetime_birth, 2),
                         name=str(target_user) + "." + str(chat_id) + "." + str(datetime_birth),
                         args=[bot, chat_id, target_user])
        sheduler.add_job(send_update_wishes,
                         trigger='date',
                         next_run_time=setDateCreate(setDateCreate(datetime_birth, 1), 1),
                         name=str(target_user) + "." + str(chat_id) + "." + str(datetime_birth),
                         args=[bot, target_user])


#async def test(bot: Bot):
#    chat_id = -4146508283
#    target_user = 841244380
#    date = database_manager.get_target_birthdays(target=target_user)
#    caption_now = "Сегодня {} празднует день рождение!"
#    sheduler.add_job(sendMessageTarget,
#                     trigger='date',
#                     next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=6),
#                     name=str(target_user) + "." + str(chat_id), args=[bot, chat_id, target_user, caption_now])
#    sheduler.add_job(bot_send_message,
#                     trigger='date',
#                     next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=6),
#                     name=str(target_user) + "." + str(chat_id), args=[bot, chat_id, target_user])
#    sheduler.add_job(send_update_wishes,
#                     trigger='date',
#                     next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=6),
#                     name=str(target_user) + "." + str(chat_id), args=[bot, target_user])
#    sheduler.add_job(deleteGroup_target, trigger='date',
#                     next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=60), args=[target_user])
#