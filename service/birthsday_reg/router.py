from aiogram import Router
from aiogram import types
from aiogram import F

import json

birthday = Router(name="birthday_register")


@birthday.message(F.text == "Регистрация")
async def birthday_start(msg: types.Message):
    await msg.answer("Заполните форму")


@birthday.message()
async def parseJSON(msg: types.Message):
    if "/parseJSON" in msg.text:
        stroka = '"' + msg.text[10:] + '"'
        print(json.loads(stroka))

# requirement
