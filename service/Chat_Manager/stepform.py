from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    LINK_CHAT = State()
