import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
import yt_dlp

# Render веб-сервер талап кылгандыктан, фондо кичинекей сервер иштетебиз
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# Токен түздөн-түз кодго жазылды, эч кандай кошумча настройка керек эмес
TOKEN = "8512153775:AAEYEpsFvQuN3KM-MrvIW_TttYYqusd8G9g"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "✨ <b>Добро пожаловать в мир музыки и видео!</b> ✨\n\n"
        "🎬 <i>Я — твой персональный помощник для скачивания контента из YouTube.</i>\n"
        "📥 <b>Просто отправь мне ссылку на любое видео или Shorts, а я сделаю всё остальное!</b> 🚀\n\n"
        "💎 <i>Быстро, удобно и прямо здесь!</i> ✨"
    )
    await message.answer(text, parse_mode=ParseMode.HTML)

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def download_video(message: Message):
    url = message.text.strip()
    wait_msg = await message.answer("⏳ <i>Подожди немного, магия уже началась... Скачиваю видео 📥...</i>", parse_mode=ParseMode.HTML)

    ydl_opts = {
    'format': 'best',
    'noplaylist': True,
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web']
        }
    }
    }
    

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        from aiogram.types import FSInputFile
        file_to_send = FSInputFile(filename)
        await message.answer_video(
            file_to_send, 
            caption="🎉 <b>Готово! Твое видео успешно скачано!</b> 🌟\n✨ <i>Приятного просмотра!</i> 🍿",
            parse_mode=ParseMode.HTML
        )
        
        if os.path.exists(filename):
            os.remove(filename)
            
        await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)

    except Exception as e:
        await message.answer(
            f"❌ <b>Упс! Произошла ошибка при скачивании:</b>\n"
            f"<code>{str(e)}</code>\n\n"
            f"💡 <i>Попробуй отправить другую ссылку!</i> ✨",
            parse_mode=ParseMode.HTML
        )
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
        except:
            pass

@dp.message()
async def echo_handler(message: Message):
    await message.answer(
        "🤖 <b>Я жду твою ссылку!</b>\n"
        "🎵 <i>Отправь мне ссылку на YouTube-видео или Shorts, чтобы начать загрузку!</i> 🚀",
        parse_mode=ParseMode.HTML
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
