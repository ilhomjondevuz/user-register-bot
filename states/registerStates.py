from aiogram.fsm.state import StatesGroup, State


class RegisterStates(StatesGroup):
    first_name = State()
    phone_number = State()
