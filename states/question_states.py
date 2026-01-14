from aiogram.fsm.state import StatesGroup, State


class AddTest(StatesGroup):
    question = State()
    answer = State()