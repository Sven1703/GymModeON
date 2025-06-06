import os
import uvicorn
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

BOT_TOKEN = "7909705556:AAG64O0ugaFSjUFpmh3oYvB55s3zcDQyfbk"
VIP_LINK = "https://www.checkout-ds24.com/redir/613899/Sven1703/"

app = FastAPI()

# Root-Route für Statuschecks (GET & HEAD)
@app.get("/")
async def root():
    return {"status": "Bot ist online! ✅"}

@app.head("/")
async def head_root():
    return Response(status_code=200)

# Telegram Bot Setup (async)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Handler definieren
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Willkommen! Sende mir 'vip', um den Link zu erhalten.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == 'private' and update.message.text.lower() == 'vip':
        await update.message.reply_text(f"🔗 Dein VIP-Link: {VIP_LINK}")

# NEU: Webhookinfo-Handler
async def webhookinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    webhook_info = await context.bot.get_webhook_info()
    msg = (
        f"🌐 Webhook-URL: {webhook_info.url or 'Nicht gesetzt'}\n"
        f"📩 Ausstehende Updates: {webhook_info.pending_update_count}\n"
        f"⚠️ Letzte Fehlermeldung: {webhook_info.last_error_message or 'Keine'}"
    )
    await update.message.reply_text(msg)

# Handler registrieren
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
application.add_handler(CommandHandler("webhookinfo", webhookinfo))  # <-- NEU



# Telegram Webhook-Route
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        json_update = await request.json()
        print("Webhook hat Update erhalten:", json_update)  # <-- Hier das Debug-Log
        update = Update.de_json(json_update, application.bot)
        await application.update_queue.put(update)
        return Response(status_code=200)
    except Exception as e:
        print("Fehler im Webhook:", e)
        return Response(status_code=500)


# Funktion zum Setzen des Webhooks bei Telegram
async def set_webhook():
    domain = os.environ.get("RENDER_EXTERNAL_URL", "https://gymmodeon.onrender.com")
    webhook_url = f"{domain}/webhook"
    await application.bot.set_webhook(webhook_url)
    print(f"🌐 Webhook gesetzt auf {webhook_url}")

if __name__ == "__main__":
    import asyncio

    async def startup():
        await application.initialize()
        await set_webhook()
        await application.start()
        print("✅ Bot gestartet")

    async def shutdown():
        await application.stop()
        await application.shutdown()

    async def main():
        asyncio.create_task(startup())
        config = uvicorn.Config("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
        await shutdown()

    asyncio.run(main())
