from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from urllib.parse import unquote, urlparse, parse_qs
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import base64
import asyncio
import nest_asyncio
import uvicorn

# 👇 Paste your real bot token here
BOT_TOKEN = "8067349631:AAFN-hy9zRK1kcd7v1n0B5DuPnq0j19TqDQ"

app = FastAPI()

@app.get("/")
def home():
    return PlainTextResponse("✅ PW Link Decoder is running.")

def extract_video_id(encoded_url: str) -> str:
    try:
        parsed_url = urlparse(encoded_url)
        query = parse_qs(parsed_url.query)
        prefix = query.get("URLPrefix", [""])[0]
        if prefix:
            decoded_prefix = base64.b64decode(prefix).decode()
            return decoded_prefix.strip("/")
        return None
    except Exception:
        return None

@app.get("/live")
def decode_pw_link(q: str = ""):
    try:
        decoded_url = unquote(q)
        stream_base = extract_video_id(decoded_url)
        if stream_base:
            stream_url = f"https://stream.pwjarvis.app/hls/720/main.m3u8"
            return PlainTextResponse(stream_url)
        return PlainTextResponse("❌ Could not extract stream base.")
    except Exception as e:
        return PlainTextResponse(f"❌ Error: {e}")

# Telegram handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me your 1DM PW video link and I'll try to return a downloadable stream link.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "pw.live" in text and ".mp4" in text:
        encoded = text
        final_url = f"https://your-api-url/live?q={encoded}"
        await update.message.reply_text(f"✅ Try this in 1DM:\n{final_url}")
    else:
        await update.message.reply_text("❌ Please send a valid PW video link (.mp4).")

async def telegram_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    await app_bot.initialize()
    await app_bot.start()
    await app_bot.updater.start_polling()
    await app_bot.updater.idle()

def start_all():
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_bot())
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    start_all()
