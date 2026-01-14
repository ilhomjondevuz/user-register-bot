from aiogram.fsm.state import StatesGroup, State


class DirectionStatesGroup(StatesGroup):
    name = State()
    price = State()
