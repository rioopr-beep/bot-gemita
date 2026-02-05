import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# MASUKKAN TOKEN TERBARU ANDA DI SINI (Pastikan tidak ada spasi di awal/akhir)
TOKEN = "8414991644:AAEckOBmcKSqkkgwpppmHsF4_VxsOuY4FxU"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hi {user_name}! Welcome to Gemita's Downloader Bot. 🤖\n\n"
        "I am ready to help you download videos. Just send me a link!\n"
        "Type /help to see my features."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 *Bot Features* 🌟\n\n"
        "✅ Support 1000+ sites (YT, TikTok, IG)\n"
        "✅ High Quality & Fast\n"
        "✅ No Ads & Free\n\n"
        "Just paste your link below!",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" in url:
        await update.message.reply_text("Processing your link... Please wait. ⏳")
    else:
        await update.message.reply_text("Please send a valid link. ❌")

if __name__ == '__main__':
    try:
        app = ApplicationBuilder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        print("--- BOT GEMITA AKTIF ---")
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        print(f"Error: {e}")
