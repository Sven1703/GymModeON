import os
import logging
from flask import Flask, request, render_template, jsonify
import requests
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback_secret_key")

# Bot-Konfiguration
BOT_TOKEN = "7909705556:AAHUMqkFFSYz6LktMXmBBmUf532DUxCro44"
VIP_LINK = "https://www.checkout-ds24.com/redir/613899/Sven1703/"
WEBHOOK_URL = "https://gymmodeon-1.onrender.com"

def send_telegram_message(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None

def set_webhook_url(webhook_url):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        data = {'url': webhook_url}
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return None

def get_webhook_info():
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html', bot_token_set=True)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "telegram_vip_bot"})

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_data = request.get_json()
        if not json_data:
            logger.error("No JSON data received")
            return "No data", 400

        logger.debug(f"Received webhook data: {json_data}")

        if 'message' in json_data:
            message = json_data['message']
            chat_id = message['chat']['id']
            chat_type = message['chat']['type']
            if chat_type == 'private' and 'text' in message:
                text = message['text'].lower().strip()
                if text == '/start':
                    response_text = "Hello! Send me 'vip' to get your VIP link!"
                    send_telegram_message(chat_id, response_text)
                elif 'vip' in text:
                    response_text = f"ð Here's your VIP link: {VIP_LINK}"
                    send_telegram_message(chat_id, response_text)

        return "OK", 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return "Error", 500

@app.route('/webhook', methods=['GET'])
def webhook_get():
    return jsonify({"message": "Webhook endpoint is active", "method": "GET"})

@app.route('/set_webhook', methods=['POST'])
def set_webhook():
    try:
        webhook_url = f"{WEBHOOK_URL}/webhook"
        result = set_webhook_url(webhook_url)
        if result and result.get('ok'):
            return jsonify({"message": f"Webhook set successfully to {webhook_url}"})
        else:
            error_msg = result.get('description', 'Failed to set webhook') if result else 'Failed to set webhook'
            return jsonify({"error": error_msg}), 500
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhook_info', methods=['GET'])
def webhook_info():
    try:
        result = get_webhook_info()
        if result and result.get('ok'):
            webhook_data = result.get('result', {})
            return jsonify({
                "url": webhook_data.get('url', ''),
                "has_custom_certificate": webhook_data.get('has_custom_certificate', False),
                "pending_update_count": webhook_data.get('pending_update_count', 0),
                "last_error_date": webhook_data.get('last_error_date'),
                "last_error_message": webhook_data.get('last_error_message'),
                "max_connections": webhook_data.get('max_connections', 40),
                "allowed_updates": webhook_data.get('allowed_updates', [])
            })
        else:
            error_msg = result.get('description', 'Failed to get webhook info') if result else 'Failed to get webhook info'
            return jsonify({"error": error_msg}), 500
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Telegram VIP Bot")
    app.run(host='0.0.0.0', port=5000, debug=True)
