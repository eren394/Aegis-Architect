import socket
import json
import sqlite3
import os
import joblib
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

UDP_IP = "127.0.0.1"
DATA_PORT = 12345
COMMAND_PORT = 12346
DB_PATH = 'data/aegis_records.db'
MODEL_PATH = "models/aegis_brain.pkl"

if not os.path.exists('data'): os.makedirs('data')
if not os.path.exists('models'): os.makedirs('models')

def core_logic():
    print("🧠 Core Logic Aktif: UDP Dinleniyor...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, DATA_PORT))
    cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    ai_model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS telemetry (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT (DATETIME('now', 'localtime')), voltage REAL, current REAL, is_anomaly INTEGER)")

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = json.loads(data.decode())
            v, c = msg["voltage"], msg["current"]
            
            is_anomaly = 0
            if ai_model:
                is_anomaly = int(ai_model.predict([[v, c]])[0])
            
            if is_anomaly == 1:
                cmd_sock.sendto(b"/SHUTDOWN", (UDP_IP, COMMAND_PORT))

            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO telemetry (voltage, current, is_anomaly) VALUES (?, ?, ?)", (v, c, is_anomaly))
            
            socketio.emit('update', {'v': v, 'c': c, 'danger': is_anomaly})
            print(f"✔️ Veri Islendi: {v}V")
            
            
        except Exception as e:
            print(f"❌ Dongu Hatası: {e}")
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    t = threading.Thread(target=core_logic, daemon=True)
    t.start()
    print("🌐 Web Sunucusu Başlatılıyor: http://127.0.0.1:5000")
    socketio.run(app, host='127.0.0.1', port=5000, debug=True, use_reloader=False)