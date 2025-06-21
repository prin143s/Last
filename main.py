from flask import Flask, request, redirect
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

BOT_TOKEN = "paste-your-telegram-bot-token-here"
API_BASE = "https://web-production-ccaed.up.railway.app/live"

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ PW Redirect API is live"

@flask_app.route("/live")
def redirector():
    url = request.args.get("q")
    if url:
        return redirect(url, code=302)
    return "❌ Invalid URL"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a PW .mp4 lecture link and I'll return a 1DM-compatible download link.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "pw.live" in text and ".mp4" in text:
        final_link = f"{API_BASE}?q={text}"
        await update.message.reply_text(f"✅ Paste this in 1DM:\n{final_link}")
    else:
        await update.message.reply_text("❌ Please send a valid PW .mp4 link.")

async def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    return app

async def start_flask():
    import nest_asyncio
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    nest_asyncio.apply()
    config = Config()
    config.bind = ["0.0.0.0:8080"]
    await serve(flask_app, config)

async def main():
    bot = await start_bot()
    await asyncio.gather(
        start_flask()
    )

if __name__ == "__main__":
    asyncio.run(main())
