from aiogram import F
from aiogram.types import Message

from keyboards.inline import directions_menu
from loader import dp


@dp.message(F.text == "📃 O'qishga topshirish")
async def submission_doc(message: Message):
    await message.answer("Iltimos yo'nalishni tanlang:", reply_markup=await directions_menu())