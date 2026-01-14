from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api.database import db


async def directions_menu():
    directions = await db.select_directions()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'{obj["name"]} | Kontrakt: {obj["contract"]}'
                )
            ]
            for obj in directions
        ]
    )

    return keyboard
