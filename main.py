from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, PlainTextResponse
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import nest_asyncio
import uvicorn

BOT_TOKEN = "8067349631:AAFN-hy9zRK1kcd7v1n0B5DuPnq0j19TqDQ"
API_BASE = "https://web-production-ccaed.up.railway.app/live"

app = FastAPI()

@app.get("/")
async def home():
    return PlainTextResponse("✅ PW Redirect API is live (FastAPI version)")

@app.get("/live")
async def redirector(q: str = None):
    if q:
        return RedirectResponse(url=q)
    return PlainTextResponse("❌ Invalid URL", status_code=400)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a PW .mp4 lecture link and I'll return a 1DM-compatible download link.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "pw.live" in text and ".mp4" in text:
        final_link = f"{API_BASE}?q={text}"
        await update.message.reply_text(f"✅ Paste this in 1DM:\n{final_link}")
    else:
        await update.message.reply_text("❌ Please send a valid PW .mp4 link.")

async def telegram_bot():
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()
    await bot_app.updater.idle()

def start_all():
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_bot())
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    start_all()
