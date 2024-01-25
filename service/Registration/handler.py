from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.enums import ParseMode

from database.database import database_manager
from service.utils.filter import IsTrueDialog
from .filter import RegistrationFilter, IsRegister
from .stepform import StepsForm
from .utils import service
from ..utils.scheduler import sendDayInChat

birthday = Router(name="birthday_register")


@birthday.message(IsTrueDialog(), Command(commands='register'))
async def birthday_start(msg: Message, state: FSMContext):
    if not await service.isRegistration(user_id=msg.from_user.id):
        await msg.answer(text="<b>Давайте заполним небольшую форму</b>\nПожалуйста, введите ваше имя",
                         parse_mode=ParseMode.HTML)
        await state.set_state(StepsForm.GET_NAME)
    else:
        await msg.answer("<b>Вы уже зарегистрированы</b>", parse_mode=ParseMode.HTML)


# Иван
@birthday.message(StepsForm.GET_NAME)
async def birthday_get_name(msg: Message, state: FSMContext):
    if len(msg.text) > 30:
        await msg.answer("Ограничение 30 символов")
        return
    await state.update_data(name=msg.text)
    await msg.answer(f"<b>{msg.text}, рад что вы присоединились к нам</b>"
                     f"\nОстался всего лишь один шаг до получения подарочков\n"
                     f"Введите. свою дату рождения в формате ДД-ММ-ГГГГ:", parse_mode=ParseMode.HTML)
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
        await msg.answer(f"<b>{name}, вы родились {date}?</b> \n Всё правильно?",
                         reply_markup=markup,
                         parse_mode=ParseMode.HTML)
        await state.set_state(StepsForm.GET_YESNO)
    else:
        await msg.answer("Введи дату правильно :с")


@birthday.callback_query(StepsForm.GET_YESNO)
async def add_user_end(call: CallbackQuery, state: FSMContext, bot: Bot):
    if call.data == '1':
        context = await state.get_data()
        await service.add_user(user_id=call.from_user.id, login=call.from_user.username, date=context['date'],
                               name=context['name'])
        await state.clear()
        await sendDayInChat(bot, target_user=call.from_user.id)
        await call.message.answer("<b>Я внёс день рождение в свой календарик</b> 🥳\n"
                                  "Если хочешь что бы тебе подарили что то конкретное, создай свой виш лист - /wishes",
                                  parse_mode=ParseMode.HTML)
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
        await call.answer()
        await state.clear()
        await call.message.answer("Нам грустно расставаться. Спасибо, что провели время с нами!")
    else:
        await call.message.answer("Очень мудрое решение с вашей стороны, спасибо что вы с нами")
        await call.answer()
        await state.clear()


@birthday.message(IsTrueDialog(), IsRegister(),Command(commands='wishes'))
async def set_wishes(msg: Message, state: FSMContext):
    try:
        a = database_manager.get_about(msg.from_user.id)[0]
    except:
        a = " Пусто "
    async def update():
        await state.set_state(StepsForm.UPDATE_ABOUT)
        return "Update"
    if a is None:
        a = "*пусто*"
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Обновить",
                                 callback_data=await update())
        ]
    ])
    await msg.answer(text=f"<b>Ваш текущий виш лист:</b> {a}", reply_markup=markup, parse_mode=ParseMode.HTML)


@birthday.callback_query(StepsForm.UPDATE_ABOUT)
async def update_wishes(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Пожалуйста введите ваши пожелания 🤔\n"
                              "<blockquote>Отменить можно с помощью команды /cancel</blockquote>", parse_mode=ParseMode.HTML)
    await call.answer()
    await state.clear()
    await state.set_state(StepsForm.UPDATE_ABOUT1)


@birthday.message(StepsForm.UPDATE_ABOUT1)
async def set_new_about(msg: Message, state: FSMContext):
    if msg.text != '/cancel':
        database_manager.update_about(msg.from_user.id, msg.text)
        await msg.answer(text="Я успешно обновил виш лист 🤗")
        await service.send_new_about(msg.from_user.id,msg.text)
    else:
        await msg.answer(text="Оставим всё как было 😬")

    await set_wishes(msg, state)
