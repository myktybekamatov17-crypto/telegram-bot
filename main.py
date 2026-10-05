import os
import asyncio
from aiogram import Bot, Dispatcher, F, types
from yt_dlp import YoutubeDL

# Ботуңуздун токенин бул жерге жазасыз же переменнаядан аласыз
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text.startswith("/start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Я могу скачать видео/Shorts с YouTube.\n"
        "Просто отправь мне ссылку!"
    )

@dp.message(F.text.startswith("http"))
async def download_video(message: types.Message):
    url = message.text.strip()
    await message.answer("⏳ Скачиваю видео, подождите немного...")

    output_file = "video.mp4"
    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': output_file,
        'max_filesize': 50 * 1024 * 1024,
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        
        'geo_bypass': True,
    }

    try:
        def download():
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        await asyncio.to_thread(download)

        if os.path.exists(output_file):
            video_file = types.FSInputFile(output_file)
            await message.answer_video(video_file)
            os.remove(output_file)
        else:
            await message.answer("❌ Не удалось найти скачанный файл.")
    except Exception as e:
        await message.answer(f"❌ Произошла ошибка при скачивании: {e}")
        if os.path.exists(output_file):
            os.remove(output_file)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
