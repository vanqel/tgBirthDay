from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from .stepform import StepsForm
from .utils import service
from .filter import RegistrationFilter, IsRegister
from service.utils.filter import IsTrueDialog
from ..utils.scheduler import sendDayInChat
birthday = Router(name="birthday_register")


@birthday.message(IsTrueDialog(), RegistrationFilter())
async def birthday_start(msg: Message, state: FSMContext):
    if not await service.isRegistration(user_id=msg.from_user.id):
        await msg.answer("Заполните форму")
        await msg.answer("Введите ваше имя:")
        await state.set_state(StepsForm.GET_NAME)
    else:
        await msg.answer("Вы уже зарегистрированы")


# Иван
@birthday.message(StepsForm.GET_NAME)
async def birthday_get_name(msg: Message, state: FSMContext):
    if len(msg.text) > 30:
        await msg.answer("Ограничение 30 символов")
        return
    await state.update_data(name=msg.text)
    await msg.answer(f"Привет {msg.text}")
    await msg.answer("Введите свою дату рождения в формате ДД-ММ-ГГГГ:")
    await state.set_state(StepsForm.GET_DATE)


# ата
@birthday.message(StepsForm.GET_DATE)
async def birthday_get_date(msg: Message, state: FSMContext):
    valide = service.validate_date(msg.text)
    if valide[0]:
        await state.update_data(date=valide[1])
        context_data = await state.get_data()
        name = context_data.get('name')
        date = context_data.get('date')
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да",
                    callback_data='1'
                )
            ],
            [
                InlineKeyboardButton(
                    text="Нет",
                    callback_data='0'
                )
            ]
        ])
        await msg.answer(f"Привет {name}, Ты родился {date}? \n Всё правильно?", reply_markup=markup)
        await state.set_state(StepsForm.GET_YESNO)
    else:
        await msg.answer("Введи дату правильно :с")


@birthday.callback_query(StepsForm.GET_YESNO)
async def add_user_end(call: CallbackQuery, state: FSMContext,bot:Bot):
    if call.data == '1':
        context = await state.get_data()
        await service.addUser(user_id=call.from_user.id, login=call.from_user.username, date=context['date'],
                              name=context['name'])
        await state.clear()
        await sendDayInChat(bot,target_user=call.from_user.id,name=context['name'])
        await call.message.answer("Я внёс твоё день рождение в свой календарик :)")
    else:
        await call.message.answer("Давайте начнём заново.\nВведите своё имя:")
        await state.set_state(StepsForm.GET_NAME)
    await call.answer()


@birthday.message(IsTrueDialog(), IsRegister(), Command(commands='clearme'))
async def delete_user_start(msg: Message, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Да",
                callback_data='1'
            )
        ],
        [
            InlineKeyboardButton(
                text="Нет",
                callback_data='0'
            )
        ]
    ])
    await msg.answer("Вы уверены?", reply_markup=markup)

    await state.set_state(StepsForm.DELETE_USER)


@birthday.callback_query(StepsForm.DELETE_USER)
async def delete_user_end(call: CallbackQuery, state: FSMContext):
    if call.data == '1':
        await service.deleteUser(call.from_user.id)
        await call.answer('НУ ТЫ И ГНИДА БЛЯТЬ')
        await state.clear()
        await call.message.answer("Нам грустно расставаться. Спасибо, что провели время с нами!")
    else:
        await call.message.answer("Очень мудрое решение с вашей стороны, спасибо что вы с нами")
        await call.answer()
        await state.clear()
