import asyncio
import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Render порту үчүн жөнөкөй веб-сервер (порт катасын алдын алуу үчүн)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Серверди өзүнчө агымда (поток) иштетүү
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Telegram боттун бөлүгү
TOKEN = "8512153775:AAHJ-pYc7Iy-oyK_3bW2_GLaHb6RBxuNbZ0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Салам! Мен музыка жана видео жүктөп берүүчү ботмун.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
