import socket
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sqlite3
import os
import joblib

UDP_IP = "127.0.0.1"
DATA_PORT = 12345
COMMAND_PORT = 12346
MODEL_PATH = "models/aegis_brain.pkl"

if not os.path.exists('data'): os.makedirs('data')
db_conn = sqlite3.connect('data/aegis_records.db', check_same_thread=False)
cursor = db_conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS telemetry (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT (DATETIME('now', 'localtime')), voltage REAL, current REAL, is_anomaly INTEGER)")
db_conn.commit()

ai_model = None
if os.path.exists(MODEL_PATH):
    ai_model = joblib.load(MODEL_PATH)
    print("AI Modeli yüklendi. Aegis artik dusunebiliyor.")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, DATA_PORT))
sock.setblocking(False)

cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fig, ax = plt.subplots()
plt.style.use('dark_background')
voltages = [220.0] * 30

def update(frame):
    try:
        data, addr = sock.recvfrom(1024)
        msg = json.loads(data.decode())
        v, c = msg["voltage"], msg["current"]
        
        is_anomaly = 0
        if ai_model:
            prediction = ai_model.predict([[v, c]])
            is_anomaly = int(prediction[0])
            print(f"Voltaj: {v:.2f} | AI Tahmini: {'TEHLIKE' if is_anomaly else 'GÜVENLİ'}")
        
        if is_anomaly == 1:
            print(f"AI TEHLIKE SEZDI: {v}V - Kapatiliyor...")
            cmd_sock.sendto(b"/SHUTDOWN", (UDP_IP, COMMAND_PORT))

        cursor.execute("INSERT INTO telemetry (voltage, current, is_anomaly) VALUES (?, ?, ?)", (v, c, is_anomaly))
        db_conn.commit()

        voltages.append(v)
        if len(voltages) > 50: voltages.pop(0)

        ax.clear()
        ax.plot(voltages, color='#00ffcc')
        ax.set_title(f"Aegis AI Control - Status: {'DANGER' if is_anomaly else 'SAFE'}")
        ax.set_ylim(150, 300)
    except:
        pass

ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
plt.show()