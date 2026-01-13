from aiogram import types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.default import send_phone
from loader import dp
from states.registerStates import RegisterStates
from utils.db_api.database import db


@dp.message(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    user = await db.select_user(int(message.from_user.id))
    if user:
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}")
    else:
        await message.answer(
            f"Salom, {message.from_user.full_name}!\n"
            f"Ism-familiyangizni kiriting:"
        )
        await state.set_state(RegisterStates.first_name)


@dp.message(StateFilter(RegisterStates.first_name))
async def first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("📱 Telefon raqamingizni yuboring", reply_markup=await send_phone())
    await state.set_state(RegisterStates.phone_number)


@dp.message(StateFilter(RegisterStates.phone_number), F.contact)
async def phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    data = await state.get_data()

    await db.insert_user(
        tg_id=message.from_user.id,
        first_name=data.get("first_name"),
        phone_number=phone_number
    )

    await message.answer(
        f"✅ {message.from_user.full_name}, siz muvaffaqqiyatli ro'yxatdan o'tdingiz!",
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.clear()
