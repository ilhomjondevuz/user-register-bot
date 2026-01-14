from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline import directions_menu
from keyboards.inline.directions_menu import DirectionCallbackData
from loader import dp


@dp.message(F.text == "📃 O'qishga topshirish")
async def submission_doc(message: Message):
    await message.answer("Iltimos yo'nalishni tanlang:", reply_markup=await directions_menu())

@dp.callback_query(DirectionCallbackData.filter())
async def direction_choices(call: CallbackQuery, state: FSMContext):
    data = call.data
    await state.set_data({
        'direction_id': int(data[-3]),
    })
    await call.message.edit_reply_markup("O'qishga topshirildi endi imtihon topshiring")