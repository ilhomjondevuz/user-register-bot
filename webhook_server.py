import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT", 3000))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())  # FSM storage kerak bo‘lsa

# Import handlers
import handlers  # sizning handlers package

async def handle(request: web.Request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return web.Response()

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    print("Webhook set:", WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle)

app.on_startup.append(on_startup)
app.on_cleanup.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, host=APP_HOST, port=APP_PORT)
