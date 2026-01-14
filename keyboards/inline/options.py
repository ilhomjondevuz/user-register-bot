from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def options():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="A", callback_data="a"),
                InlineKeyboardButton(text="B", callback_data="b"),
            ],[
                InlineKeyboardButton(text="C", callback_data="c"),
                InlineKeyboardButton(text="D", callback_data="d"),
            ],
        ]
    )
