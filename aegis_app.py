import json
import logging
import socket
import sqlite3
import threading
from pathlib import Path

import joblib
from flask import Flask, render_template
from flask_socketio import SocketIO

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

UDP_IP = "127.0.0.1"
DATA_PORT = 12345
COMMAND_PORT = 12346
DB_PATH = DATA_DIR / "aegis_records.db"
MODEL_PATH = MODELS_DIR / "aegis_brain.pkl"

app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

def core_logic():
    logging.info("🧠 Core Logic aktif: UDP dinleniyor")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, DATA_PORT))
    cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    ai_model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None
    if ai_model is None:
        logging.warning("Model bulunamadı, sistem sadece telemetry kaydı yapacak: %s", MODEL_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT (DATETIME('now', 'localtime')),
            voltage REAL,
            current REAL,
            is_anomaly INTEGER
        )
        """
    )
    conn.commit()

    try:
        while True:
            try:
                data, _ = sock.recvfrom(1024)
                msg = json.loads(data.decode())
                v, c = float(msg["voltage"]), float(msg["current"])

                is_anomaly = int(ai_model.predict([[v, c]])[0]) if ai_model else 0

                if is_anomaly == 1:
                    cmd_sock.sendto(b"/SHUTDOWN", (UDP_IP, COMMAND_PORT))

                conn.execute(
                    "INSERT INTO telemetry (voltage, current, is_anomaly) VALUES (?, ?, ?)",
                    (v, c, is_anomaly),
                )
                conn.commit()

                socketio.emit('update', {'v': v, 'c': c, 'danger': is_anomaly})
                logging.info("✔️ Veri işlendi: %.2fV | %.2fA | anomaly=%s", v, c, is_anomaly)

            except (json.JSONDecodeError, KeyError, ValueError) as err:
                logging.warning("Geçersiz telemetry paketi alındı: %s", err)
            except Exception:
                logging.exception("❌ Döngü hatası")
    finally:
        conn.close()
        sock.close()
        cmd_sock.close()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    t = threading.Thread(target=core_logic, daemon=True)
    t.start()
    logging.info("🌐 Web sunucusu başlatılıyor: http://127.0.0.1:5000")
    socketio.run(app, host='127.0.0.1', port=5000, debug=True, use_reloader=False)
