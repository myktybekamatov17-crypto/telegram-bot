import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
import yt_dlp

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

TOKEN = "8512153775:AAHJ-pYc7Iy-oyK_3bW2_GLaHb6RBXunBZ0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "👋 Салам! Кош келиңиз!\n\n"
        "🎬 Мен YouTube'дан музыка жана видео көчүрүүчү ботмун.\n"
        "📥 Мага видеонун же шортстун шилтемесин жибериңиз, мен аны сиз үчүн көчүрүп берем! 🚀"
    )
    await message.answer(text)

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def download_video(message: Message):
    url = message.text.strip()
    wait_msg = await message.answer("⏳ Сураныч, күтүп туруңуз... Видеону көчүрүп жатам 📥...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        from aiogram.types import FSInputFile
        file_to_send = FSInputFile(filename)
        await message.answer_video(file_to_send, caption="✅ Мына сиздин видео! Жакшы көрүңүз! 🎉")
        
        if os.path.exists(filename):
            os.remove(filename)
            
        await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)

    except Exception as e:
        await message.answer(f"❌ Көчүрүү учурунда ката кетти:\n{str(e)}\n\n💡 Башка шилтеме сынап көрүңүз!")
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
        except:
            pass

@dp.message()
async def echo_handler(message: Message):
    await message.answer("🤖 Видеону көчүрүү үчүн мага YouTube шилтемесин жибериңиз! 🎵🎥")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    
