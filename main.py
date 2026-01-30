import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# ====== IMPORTANT VARIABLES ======
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()

# ====== TELEGRAM APP ======
telegram_app = Application.builder().token(TOKEN).build()


# ====== COMMAND: /start ======
async def start(update: Update, context):
    await update.message.reply_text("👋 Hello! Send me any message and I'll echo it back.")


# ====== ECHO HANDLER ======
async def echo(update: Update, context):
    text = update.message.text
    await update.message.reply_text(f"📝 You said: {text}")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# ====== WEBHOOK ROUTE ======
@app.post("/")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}


# ====== STARTUP EVENT ======
@app.on_event("startup")
async def on_startup():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)


# ====== SHUTDOWN EVENT ======
@app.on_event("shutdown")
async def on_shutdown():
    await telegram_app.shutdown()
