import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token Anda
TOKEN = "8414991644:AAEckOBmcKSqkkgwpppmHsF4_VxsOuY4FxU"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi Gemita! Send me a YouTube link and I will send you the video file. 📥")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url:
        await update.message.reply_text("Please send a valid link. ❌")
        return

    status_msg = await update.message.reply_text("📥 Downloading... please wait. This may take a while.")

    # Folder sementara untuk menyimpan video
    output_file = "video.mp4"

    # Pengaturan yt-dlp (Cepat & MP4)
    ydl_opts = {
        'format': 'best[ext=mp4]/best', # Ambil MP4 terbaik
        'outtmpl': output_file,
        'max_filesize': 45000000, # Batas 45MB agar tidak ditolak Telegram
    }

    try:
        # Proses Mengunduh
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Proses Mengirim ke Telegram
        await status_msg.edit_text("📤 Sending to Telegram...")
        with open(output_file, 'rb') as video:
            await update.message.reply_video(video=video, caption="Success! Here is your video. ✅")
        
        # Hapus file setelah terkirim agar server tidak penuh
        os.remove(output_file)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("--- BOT GEMITA RUNNING ---")
    app.run_polling(drop_pending_updates=True)
