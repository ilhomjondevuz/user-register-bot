from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def add_direction():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎓 Yo'nalish qo'shish")
            ],
            [
                KeyboardButton(text="➕ Test qo'shish")
            ]
        ],
        resize_keyboard=True
    )
