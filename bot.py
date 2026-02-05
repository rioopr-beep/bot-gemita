import os
import asyncio
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram.request import HTTPXRequest

# Token Gemita
TOKEN = '8414991644:AAGJoDULW5KvqdFZwZUJ0QdlSmYZWpPzFhQ'

async def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best', 
        'outtmpl': 'video_downloaded.%(ext)s', 
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = await asyncio.to_thread(ydl.extract_info, url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith('http'): return
    status = await update.message.reply_text("Sedang diproses server cloud... ⏳")
    try:
        file_path = await download_video(url)
        with open(file_path, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption="Ini videonya, Gemita! ✨")
        if os.path.exists(file_path): os.remove(file_path)
        await status.delete()
    except Exception as e:
        print(f"Error: {e}")
        await status.edit_text("Gagal mengunduh. Link mungkin tidak didukung atau server sibuk.")

if __name__ == '__main__':
    print("--- MEMULAI BOT DI SERVER CLOUD ---")
    request_config = HTTPXRequest(connect_timeout=60, read_timeout=60)
    app = ApplicationBuilder().token(TOKEN).request(request_config).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("--- BOT GEMITA SUDAH AKTIF ---")
    app.run_polling()
