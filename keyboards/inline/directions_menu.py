from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api.database import db
from aiogram.filters.callback_data import CallbackData


class DirectionCallbackData(CallbackData, prefix="directions"):
    id: int
    step: int


async def directions_menu():
    directions = await db.select_directions()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for direction in directions:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f'{direction["name"]} kontrakt: {direction["contract"]} so\'m',
                callback_data=DirectionCallbackData(
                    id=direction["id"],
                    step=0
                ).pack()
            )
        ])

    return keyboard
