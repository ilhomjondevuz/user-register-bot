import asyncio
import logging
import sys

from loader import dp, bot
import middlewares, filters, handlers
from utils.db_api import Database
from utils.db_api.database import db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup():
    # DB connection
    try:
        await db.connect()
        print("Connected")
    except Exception as e:
        print(e)

    # Birlamchi komandalar (/start va /help)
    await set_default_commands()

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify()


async def on_shutdown():
    # DB disconnect
    await db.disconnect()


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)  # 🔥 shutdown qo‘shish
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
