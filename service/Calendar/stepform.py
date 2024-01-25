from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    SEND_CALENDAR = State()
