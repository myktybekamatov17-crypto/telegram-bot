import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL
from aiohttp import web

logging.basicConfig(level=logging.INFO)

TOKEN = "8512153775:AAHJ-pYc7Iy-oyK_3bW2_GLaHb6RBxuNbZ0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Я могу поговорить с тобой или скачать видео/Shorts с YouTube.\n"
        "Просто отправь мне ссылку!"
    )

# Микро веб-сервер для Render
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def main():
    # Запускаем фоновый веб-сервер
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    # Запускаем самого бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
