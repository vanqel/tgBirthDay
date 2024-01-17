from aiogram.fsm.state import StatesGroup, State

class StepsForm(StatesGroup):
    GET_YESNO = State()
    GET_NAME = State()
    GET_DATE = State()
    DELETE_USER = State()
