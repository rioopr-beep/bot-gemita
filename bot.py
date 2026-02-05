import os
import logging
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token Gemita
TOKEN = "8414991644:AAEckOBmcKSqkkgwpppmHsF4_VxsOuY4FxU"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Aktif! Silakan kirim link video YouTube atau TikTok, 😊")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url:
        return

    # Pesan status agar user tahu bot bekerja
    progress_msg = await update.message.reply_text("⏳ Sedang mengunduh... Mohon tunggu sebentar.")
    
    file_name = f"video_{update.effective_user.id}.mp4"
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': file_name,
        'max_filesize': 48000000, # Batasi 48MB (Limit Telegram 50MB)
    }

    try:
        # Menjalankan download di background agar tidak membekukan bot
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))

        if os.path.exists(file_name):
            await progress_msg.edit_text("📤 Mengirim file ke Telegram...")
            with open(file_name, 'rb') as v:
                await update.message.reply_video(video=v, caption="Ini videonya, ! ✅")
            os.remove(file_name) # Hapus file setelah kirim
            await progress_msg.delete()
        else:
            await progress_msg.edit_text("❌ Gagal mengunduh video. Mungkin file terlalu besar (>50MB).")

    except Exception as e:
        await progress_msg.edit_text(f"❌ Terjadi kesalahan: {str(e)}")
        if os.path.exists(file_name): os.remove(file_name)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(drop_pending_updates=True)
