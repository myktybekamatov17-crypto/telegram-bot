import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
import yt_dlp

# Render порт талабын аткаруу үчүн жөнөкөй веб-сервер
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Веб-серверди өзүнчө агымда (thread) кошобуз
threading.Thread(target=run_web_server, daemon=True).start()

# Тектирүүчү токен (өзүңүздүн бот токениңиз)
TOKEN = "8512153775:AAHS... (өз токениңизди жазыңыз)" 
# Эскертүү: Токениңизді өзүңүздүн иштеп жаткан токениңизге алмаштырыңыз же мурунку коддогудай калтырыңыз.

bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start буйругуна орусча жана смайликтер менен жооп берүү
@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "👋 Привет! Добро пожаловать!\n\n"
        "🎬 Я бот для скачивания музыки и видео из YouTube.\n"
        "📥 Просто отправь мне ссылку на видео или шортс, а я скачаю его для тебя! 🚀"
    )
    await message.answer(text)

# YouTube шилтемелерин кармап алып скачать этүү
@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def download_video(message: Message):
    url = message.text.strip()
    wait_msg = await message.answer("⏳ Пожалуйста, подожди... Скачиваю видео 📥...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'max_filesize': 50 * 1024 * 1024, # Telegram чектөөсү үчүн (50МБ)
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Видео файлды Telegram аркылуу жиберүү
        from aiogram.types import FSInputFile
        file_to_send = FSInputFile(filename)
        await message.answer_video(file_to_send, caption="✅ Вот твое видео! Приятного просмотра! 🎉")
        
        # Жүктөлүп бүткөн соң серверден файлды өчүрүү
        if os.path.exists(filename):
            os.remove(filename)
            
        await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)

    except Exception as e:
        await message.answer(f"❌ Ошибка при скачивании:\n{str(e)}\n\n💡 Попробуй другую ссылку!")
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
        except:
            pass

# Калган тексттерге жооп
@dp.message()
async def echo_handler(message: Message):
    await message.answer("🤖 Отправь мне ссылку на YouTube-видео, чтобы я мог скачать его для тебя! 🎵🎥")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    
