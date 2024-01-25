# import logging
# import random
# from time import sleep
#
# from aiogram import Bot
# from pyrogram import Client, filters
# from pyrogram.enums import ParseMode
# from pyrogram.errors import FloodWait
#
# from database.database import database_manager
# from config import *
# from service.utils.utils import get_photo_user_bin, logger
#
# app = Client(name="Ассистент BirthdayCSAT", api_id=API_ID, api_hash=API_HASH)
#
#
#
# logging.basicConfig(level=logging.INFO)
# app = Client(name="Ассистент BirthdayCSAT", api_id=API_ID, api_hash=API_HASH)
# async def create():
#   try:
#       await app.start()
#       chat = await app.create_group(title="Группачка", users=[841244380])
#       invite_link = await chat.export_invite_link()
#       print(invite_link)
#       await app.stop()
#   except Exception as e:
#       print(f"Произошла ошибка: {e}")
# @app.on_message(filters.command("type", prefixes=".") & filters.me)
# def type(_, msg):
#   orig_text = msg.text.split(".type ", maxsplit=1)[1]
#   text = orig_text
#   tbp = ""  # to be printed
#   typing_symbol = "▒"
#   while (tbp != orig_text):
#       try:
#           msg.edit(tbp + typing_symbol)
#           sleep(0.05)  # 50 ms
#           tbp = tbp + text[0]
#           text = text[1:]
#           msg.edit(tbp)
#           sleep(0.05)
#       except FloodWait as e:
#           sleep(e.x)
#
# @app.on_message(filters.command("hack", prefixes=".") & filters.me)
# def hack(_, msg):
#   perc = 0
#   while (perc < 100):
#       try:
#           text = "👮‍ Взлом пентагона в процессе ..." + str(perc) + "%"
#           msg.edit(text)
#           perc += random.randint(1, 3)
#           sleep(0.1)
#       except FloodWait as e:
#           sleep(e.x)
#   msg.edit("🟢 Пентагон успешно взломан!")
#   sleep(3)
#   msg.edit("👽 Поиск секретных данных об НЛО ...")
#   perc = 0
#   while (perc < 100):
#       try:
#           text = "👽 Поиск секретных данных об НЛО ..." + str(perc) + "%"
#           msg.edit(text)
#           perc += random.randint(1, 5)
#           sleep(0.15)
#       except FloodWait as e:
#           sleep(e.x)
#   msg.edit("🦖 Найдены данные о существовании динозавров на земле!")
#
# app.run()
import datetime

from service.utils.scheduler import sheduler


def setDateCreate(date: datetime.date):

    if 10 <= date.day < 25:
        if date.month == 1:
            date = date.replace(day=25, month=12, year=date.year-1)
        else:
            date = date.replace(day=25, month=date.month - 1 )
        if date < datetime.datetime.now().date():
            return datetime.datetime.now().replace(hour=12, minute=30)
        return date

    if 25 <= date.day <= 31:
        date = date.replace(day=10)
        if date < datetime.datetime.now().date():
            return datetime.datetime.now().replace(hour=12, minute=30)
        return date

    if 1 <= date.day < 10:
        if date.month == 1:
            date = date.replace(day=10, month=12, year=date.year - 1)
        else:
            date = date.replace(day=10, month=date.month - 1)

        if date < datetime.datetime.now().date():
            return datetime.datetime.now().replace(hour=12, minute=30)
        return date


for i in range(360):
    date = datetime.date(day=1,month=1,year=2025) + datetime.timedelta(days=i)
    print(f"| {date} | {setDateCreate(date)} |")

