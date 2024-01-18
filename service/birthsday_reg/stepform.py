from aiogram.fsm.state import StatesGroup, State

class StepsForm(StatesGroup):
    GET_YESNO = State()
    GET_NAME = State()
    GET_DATE = State()
    REGISTER_YESNO = State()
    START_REG = State()
    DELETE_USER = State()
