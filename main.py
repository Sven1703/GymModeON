import os
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from http.server import HTTPServer, BaseHTTPRequestHandler

BOT_TOKEN = "7909705556:AAG64O0ugaFSjUFpmh3oYvB55s3zcDQyfbk"
VIP_LINK = "https://www.checkout-ds24.com/redir/613899/Sven1703/"

# === Bot-Funktionen ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Willkommen! Sende mir 'vip' per privater Nachricht, um deinen Link zu erhalten.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == 'private' and update.message.text.lower() == 'vip':
        await update.message.reply_text(f"🔗 Dein VIP-Link: {VIP_LINK}")

# === Webserver für UptimeRobot und Telegram Webhook ===

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

# === Hauptfunktion ===

def main():
    # Starte Webserver für UptimeRobot
    threading.Thread(target=run_webserver, daemon=True).start()

    # Hole deine Render-Domain (z. B. https://gymmodeon.onrender.com)
    domain = "https://gymmodeon.onrender.com"

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handler für Telegram
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Webhook-URL setzen (Telegram sendet dorthin)
    webhook_path = "/webhook"
    webhook_url = f"{domain}{webhook_path}"

    print(f"🌐 Setze Webhook auf: {webhook_url}")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        webhook_path=webhook_path,
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    main()
