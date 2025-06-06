import os
import threading
import asyncio
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from http.server import HTTPServer, BaseHTTPRequestHandler

BOT_TOKEN = "7909705556:AAG64O0ugaFSjUFpmh3oYvB55s3zcDQyfbk"
VIP_LINK = "https://www.checkout-ds24.com/redir/613899/Sven1703/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Willkommen! Sende mir 'vip' per privater Nachricht, um deinen Link zu erhalten.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == 'private' and update.message.text.lower() == 'vip':
        await update.message.reply_text(f"🔗 Dein VIP-Link: {VIP_LINK}")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write('Bot ist online! ✅'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Not Found'.encode('utf-8'))

def run_webserver():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

async def main():
    domain = os.environ.get("RENDER_EXTERNAL_URL", "https://gymmodeon.onrender.com")
    webhook_path = "/webhook"
    webhook_url = f"{domain}{webhook_path}"

    # Application erstellen UND initialisieren
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print(f"🌐 Setze Webhook auf: {webhook_url}")
    await app.initialize()       # WICHTIG: Application initialisieren
    await app.bot.set_webhook(webhook_url)

    # Webserver starten (für UptimeRobot)
    threading.Thread(target=run_webserver, daemon=True).start()

    # Telegram Webhook starten
    await app.start()
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        webhook_path=webhook_path
    )
    print("✅ Bot läuft mit Webhook!")
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
