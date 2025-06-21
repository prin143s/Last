from flask import Flask, request, redirect
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import threading

BOT_TOKEN = "paste-your-bot-token-here"
API_BASE = "https://web-production-ccaed.up.railway.app/live"

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ PW Redirect API is live"

@app.route("/live")
def redirector():
    url = request.args.get("q")
    if url:
        return redirect(url, code=302)
    return "❌ Invalid URL"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a PW video link (.mp4) and I’ll return a 1DM-compatible download link.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "pw.live" in text and ".mp4" in text:
        final_link = f"{API_BASE}?q={text}"
        await update.message.reply_text(f"✅ Paste this in 1DM:
{final_link}")
    else:
        await update.message.reply_text("❌ Please send a valid PW .mp4 link.")

async def run_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    await app_bot.run_polling()

def launch_bot():
    asyncio.run(run_bot())

if __name__ == "__main__":
    threading.Thread(target=launch_bot).start()
    app.run(host="0.0.0.0", port=8080)
