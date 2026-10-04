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

# Обработчик ссылок (скачивание видео)
@dp.message(F.text.startswith("http"))
async def download_video(message: types.Message):
    url = message.text.strip()
    await message.answer("⏳ Скачиваю видео, подождите немного...")

    output_file = "video.mp4"

    # Настройки yt-dlp для скачивания лучшего видео
    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': output_file,
        'max_filesize': 50 * 1024 * 1024, # Ограничение до 50 МБ для Telegram
    }

    try:
        def download():
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        # Запускаем скачивание в отдельном потоке, чтобы не вешать бота
        await asyncio.to_thread(download)

        if os.path.exists(output_file):
            await message.answer_video(types.FSInputFile(output_file))
            os.remove(output_file) # Удаляем файл после отправки
        else:
            await message.answer("❌ Не удалось найти скачанный файл.")

    except Exception as e:
        await message.answer(f"❌ Произошла ошибка при скачивании:\n{str(e)}")
        if os.path.exists(output_file):
            os.remove(output_file)

# Микро веб-сервер для Render
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
