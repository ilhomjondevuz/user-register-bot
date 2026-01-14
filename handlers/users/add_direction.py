from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from data import config
from keyboards.default import menu, add_direction
from loader import dp
from states import DirectionStatesGroup
from utils.db_api.database import db


@dp.message(F.text == "🎓 Yo'nalish qo'shish")
async def add_direction_(message: Message, state: FSMContext):
    await message.answer("Yo'nalish nomini kiriting:" , reply_markup=ReplyKeyboardRemove())
    await state.set_state(DirectionStatesGroup.name)

@dp.message(StateFilter(DirectionStatesGroup.name))
async def send_direction_name(message: Message, state: FSMContext):
    await state.set_data({
        "name": message.text
    })
    await message.answer("Yo'nalish kontrakt narxini kiriting:" , reply_markup=ReplyKeyboardRemove())
    await state.set_state(DirectionStatesGroup.price)

@dp.message(StateFilter(DirectionStatesGroup.price))
async def send_contract_price(message: Message, state: FSMContext):
    try:
        float(message.text)
    except Exception as e:
        await message.answer(str(e))
    await state.update_data({
        "contract": float(message.text)
    })
    data = await state.get_data()
    await db.add_direct(**data)
    await state.clear()
    is_admin = str(message.from_user.id) in config.ADMINS
    markup = await add_direction() if is_admin else await menu()
    await message.answer(
        f"Bosh sahifa {message.from_user.mention_html()}",
        reply_markup=markup
    )