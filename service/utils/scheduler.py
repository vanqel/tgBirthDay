import datetime

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.database import manager
from .utils import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

sheduler = AsyncIOScheduler(timezone='Europe/Moscow', executor="asyncio")


async def loadAllShedulerJob(bot: Bot):
    users = manager.getAllUsers()
    try:
        for target in users:
            await sendDayInChat(bot, target[1])
        logger("INFO: <b> ALL SCHEDULER JOBS COMPLETE</b>")
    except Exception as ex:
        logger(f"ERROR: SCHEDULER <b>{ex}</b>")
async def sendDayInChat(bot: Bot, target_user):
    chats = manager.getUserInChat(target_user)
    for chat_id in chats:
        try:
            date, users = manager.getTargetAnivers(target_user, chat_id)
            chat = await bot.get_chat(chat_id)
            chat_title = chat.title
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=f"{chat_title}",
                                         url=str(await bot.create_chat_invite_link(chat_id=chat.id)))
                ]
            ])

            async def sendMesage_5():
                try:
                    date, users = manager.getTargetAnivers(target_user, chat_id)
                    for user in users:
                        photo = await bot.get_user_profile_photos(user_id=user[0])
                        photo = photo.photos[0][0].file_id
                        await bot.send_photo(chat_id=user[0], photo=photo,
                                             caption=f"Через 5 дней у {user[1]} день рождение. Самое время "
                                                     f"начинать готовить поздравление!", reply_markup=markup)
                except Exception as ex:
                    print(ex)

            async def sendMesage_1():
                try:
                    date, users = manager.getTargetAnivers(target_user, chat_id)
                    for user in users:
                        photo = await bot.get_user_profile_photos(user_id=user[0])
                        photo = photo.photos[0][0].file_id
                        await bot.send_photo(chat_id=user[0], photo=photo,
                                             caption=f"Завтра у {user[1]}  день рождение. Надеюсь вы "
                                                     f"приготовили поздравление!", reply_markup=markup)
                except Exception as ex:
                    print(ex)

            async def sendMessageTarget():
                try:
                    date, users = manager.getTargetAnivers(target_user, chat_id)
                    for user in users:
                        photo = await bot.get_user_profile_photos(user_id=user[0])
                        photo = photo.photos[0][0].file_id
                        await bot.send_photo(chat_id=user[0], photo=photo,
                                             caption=f"Сегодня у {user[1]}  день рождение. Самое время поздравить его! ",
                                             reply_markup=markup)
                        await bot.send_message(chat_id=user[0], text=f"{user[1]}, очень сильно поздравляю тебя!!!")
                except Exception as ex:
                    print(ex)

            sheduler.add_job(sendMesage_5, trigger='date', run_date=datetime.date(month=date.month,day=date.day, year=datetime.datetime.now().year) - datetime.timedelta(days=5))
            sheduler.add_job(sendMesage_1, trigger='date', run_date=date - datetime.timedelta(days=1))
            sheduler.add_job(sendMessageTarget, trigger='date', run_date=date)

        except Exception as ex:
            print(ex)
