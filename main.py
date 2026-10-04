import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL

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

# Обработчик всех текстовых сообщений
@dp.message(F.text)
async def handle_text(message: types.Message):
    text = message.text.strip()
    text_lower = text.lower()

    if "youtube.com" in text_lower or "youtu.be" in text_lower:
        await download_video(message, text)
        return

    if any(greeting in text_lower for greeting in ["привет", "хай", "здравствуй", "салам"]):
        await message.answer("Привет-привет! Как дела? Чем помочь? 😊")
    elif "как дела" in text_lower:
        await message.answer("У меня всё отлично, работаю и готов скачивать видео! А у тебя как? 🚀")
    elif any(thanks in text_lower for thanks in ["спасибо", "благодарю", "рахмат"]):
        await message.answer("Пожалуйста! Обращайся всегда 😉")
    elif "что ты умеешь" in text_lower:
        await message.answer("Я умею скачивать видео и Shorts с YouTube! Отправь мне ссылку, и я пришлю файл 📹")
    else:
        await message.answer(
            f"Я получил твое сообщение: \"{text}\"\n\n"
            "Если хочешь скачать видео — просто отправь мне ссылку на YouTube! 🎬"
        )

# Функция скачивания видео
async def download_video(message: types.Message, url: str):
    status_msg = await message.answer("⏳ Скачиваю видео, подождите...")
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'android']
            }
        }
    }

    try:
        loop = asyncio.get_event_loop()
        
        def process_download():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        filename = await loop.run_in_executor(None, process_download)
        
        if not filename or not os.path.exists(filename):
            files = [os.path.join('downloads', f) for f in os.listdir('downloads')]
            if files:
                filename = max(files, key=os.path.getctime)
            else:
                raise Exception("Не удалось сохранить файл.")

        await status_msg.edit_text("Отправляю в Telegram... 📤")
        
        video_file = types.FSInputFile(filename)
        await message.answer_video(video=video_file, caption="✅ Успешно скачано!")
        
        if os.path.exists(filename):
            os.remove(filename)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ Ошибка скачивания: {e}")

async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
      
