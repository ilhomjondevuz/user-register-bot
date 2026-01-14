from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📃 O'qishga topshirish"),
                KeyboardButton(text="🎓 Magistraturaga hujjat topshirish")
            ],
            [
                KeyboardButton(text="📝 Imtihon topshirish"),
                KeyboardButton(text="👨‍💼 Admin bilan bog'lanish")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
