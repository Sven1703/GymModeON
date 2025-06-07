import os
import uvicorn
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

BOT_TOKEN = "7909705556:AAHUMqkFFSYz6LktMXmBBmUf532DUxCro44"
VIP_LINK = "https://www.checkout-ds24.com/redir/613899/Sven1703/"

app = FastAPI()

@app.head("/")
@app.get("/")
async def root():
    return {"status": "Bot ist online ✅"}

application = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Willkommen! Sende mir 'vip' per privater Nachricht, um deinen Link zu erhalten.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private" and update.message.text.lower() == "vip":
        await update.message.reply_text(f"🔗 Dein VIP-Link: {VIP_LINK}")
    else:
        await update.message.reply_text("❗Bitte schreibe 'vip' in einer privaten Nachricht.")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@app.post("/webhook")
async def telegram_webhook(req: Request):
    update = Update.model_validate(await req.json(), context={"bot": application.bot})
    await application.update_queue.put(update)
    return "ok"

if __name__ == "__main__":
    import asyncio

    async def start_bot():
        print("🔄 start_bot() wird ausgeführt - initialisiere Bot...")
        await application.initialize()
        webhook_url = "https://gymmodeon-1.onrender.com"  # Ersetze mit deiner Render-URL!
        await application.bot.set_webhook(webhook_url)
        await application.start()
        print(f"✅ Webhook gesetzt auf: {webhook_url}")

    async def shutdown_bot():
        await application.stop()
        await application.shutdown()

    async def main():
        asyncio.create_task(start_bot())
        config = uvicorn.Config("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
        await shutdown_bot()

    asyncio.run(main())
