from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from data import config
from keyboards.default import add_direction, menu
from keyboards.inline import options
from loader import dp
from states.question_states import AddTest
from utils.db_api.database import db
from aiogram.exceptions import TelegramBadRequest


@dp.message(F.text == "➕ Test qo'shish")
async def added_test(message: Message, state: FSMContext):
    await message.answer("Test savolini kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddTest.question)


@dp.message(F.text, StateFilter(AddTest.question))
async def added_question(message: Message, state: FSMContext):
    await state.set_data({
        "question": message.text
    })
    await message.answer("To'g'ri variantni tanlang:", reply_markup=await options())
    await state.set_state(AddTest.answer)


@dp.callback_query(AddTest.answer)
async def answer_test(query: CallbackQuery, state: FSMContext):
    await state.update_data(answer=query.data)

    # Inline keyboardni olib tashlash: faqat kerak bo‘lsa
    try:
        if query.message.text != "Savol qabul qilindi!":
            await query.message.edit_text("Savol qabul qilindi!")
        if query.message.reply_markup is not None:
            await query.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest:
        pass  # Xabar allaqachon o‘zgartirilgan bo‘lsa e'tiborsiz qoldiramiz

    # Admin yoki foydalanuvchi uchun alohida Reply/Inline keyboard yuborish
    is_admin = str(query.from_user.id) in config.ADMINS
    if is_admin:
        await query.message.answer(
            "Admin menyu",
            reply_markup=await add_direction()  # INLINE keyboard
        )
    else:
        await query.message.answer(
            "Menyu",
            reply_markup=await menu()  # REPLY keyboard
        )

    # DB ga testni qo‘shish
    data = await state.get_data()
    await db.add_test(**data)
    await state.clear()
