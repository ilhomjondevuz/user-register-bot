from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters.admins import AdminFilter
from loader import dp
from states import DirectionStatesGroup
from utils.db_api.database import db


@dp.messase(AdminFilter(), F.text == "🎓 Yo'nalish qo'shish")
async def message_doc(message: Message, state: FSMContext):
    await message.answer("Yo'nalish nomini kiriting:")
    await state.set_state(DirectionStatesGroup.name)

@dp.message(StateFilter(DirectionStatesGroup.name))
async def dd_contract_price(message: Message, state: FSMContext):
    await state.set_data({
        "direction": message.text
    })
    await message.answer("Kontrkt narxini kiriting:")
    await state.set_state(DirectionStatesGroup.price)

def text_to_float(text: str) -> float | None:
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


@dp.message(StateFilter(DirectionStatesGroup.price))
async def finish_direction(message: Message, state: FSMContext):
    data = await state.get_data()
    if text_to_float(message.text):
        data["contract"] = text_to_float(message.text)
    else:
        return

    db.add_direct(**data)
    await message.answer("Yo'nalish muvaqqiyatli qo'shildi!")
    await state.clear()
