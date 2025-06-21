from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import asyncio
import uvicorn

BOT_TOKEN = os.getenv("8067349631:AAFN-hy9zRK1kcd7v1n0B5DuPnq0j19TqDQ") or "paste-your-telegram-bot-token-here"
API_BASE = os.getenv("https://web-production-ccaed.up.railway.app/
live") or "https://your-domain.com/live"

app = FastAPI()

@app.get("/")
def home():
    return {"message": "✅ PW Redirect API is live"}

@app.get("/live")
def redirector(request: Request):
    url = request.query_params.get("q")
    if url:
        return RedirectResponse(url)
    return {"error": "❌ Invalid URL"}

# --- Telegram Bot Logic ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a PW .mp4 lecture link (from 1DM) and I’ll return a 1DM-compatible link.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "pw.live" in text and ".mp4" in text:
        final = f"{API_BASE}?q={text}"
        await update.message.reply_text(f"✅ Paste this in 1DM:\n{final}")
    else:
        await update.message.reply_text("❌ Send a valid PW .mp4 link from 1DM")

async def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

@app.on_event("startup")
def launch_bot():
    asyncio.create_task(run_bot())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
