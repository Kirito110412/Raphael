import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your AI OS. Ready for commands.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Stub: Here we would route the text into the API/LangGraph
    await update.message.reply_text(f"Received text: {text}")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Stub: Handle audio note
    await update.message.reply_text("Audio note received.")

def run_telegram_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN", "stub_token")
    if token == "stub_token" or not token:
        print("No Telegram token provided. Skipping bot initialization.")
        return

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Telegram bot started.")
    app.run_polling()

if __name__ == "__main__":
    run_telegram_bot()
