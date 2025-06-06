import os
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from http.server import HTTPServer, BaseHTTPRequestHandler

BOT_TOKEN = "7909705556:AAG64O0ugaFSjUFpmh3oYvB55s3zcDQyfbk"
VIP_LINK = "https://www.checkout-ds24.com/redir/613899/Sven1703/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Willkommen! Sende mir 'vip' per privater Nachricht, um deinen Link zu erhalten.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == 'private' and update.message.text.lower() == 'vip':
        await update.message.reply_text(f"🔗 Dein VIP-Link: {VIP_LINK}")

# Minimaler Webserver, der nichts macht, nur den Port offen hält
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_webserver():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

def main():
    # Starte den Webserver in einem separaten Thread (für Render.com)
    threading.Thread(target=run_webserver, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("✅ Bot läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()
