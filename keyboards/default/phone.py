from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


async def send_phone():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Telefon raqamni yuborish", request_contact=True),
            ]
        ],
        resize_keyboard=True)
    return markup

