import socket
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sqlite3
import os

UDP_IP = "127.0.0.1"
DATA_PORT = 12345
COMMAND_PORT = 12346 
ANOMALY_THRESHOLD = 240.0 
MAX_ANOMALY_COUNT = 5

if not os.path.exists('data'): os.makedirs('data')
db_conn = sqlite3.connect('data/aegis_records.db', check_same_thread=False)
cursor = db_conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS telemetry (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT (DATETIME('now', 'localtime')), voltage REAL, current REAL, is_anomaly INTEGER)")
db_conn.commit()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
sock.bind((UDP_IP, DATA_PORT))
sock.setblocking(False) 

cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fig, ax = plt.subplots()
voltages = [220.0] * 30 
anomaly_counter = 0

print(f"--- Aegis Mind Dinlemede: {DATA_PORT} ---")

def update(frame):
    global anomaly_counter
    try:
        data, addr = sock.recvfrom(1024)
        msg = json.loads(data.decode())
        
        v = msg["voltage"]
        c = msg["current"]
        is_anom = v > ANOMALY_THRESHOLD
        
        voltages.append(v)
        if len(voltages) > 50: voltages.pop(0) 
        
        cursor.execute("INSERT INTO telemetry (voltage, current, is_anomaly) VALUES (?, ?, ?)", (v, c, 1 if is_anom else 0))
        db_conn.commit()
        
        if is_anom:
            anomaly_counter += 1
            print(f"⚠️ KRİTİK: {v:.2f}V ({anomaly_counter}/{MAX_ANOMALY_COUNT})")
        else:
            anomaly_counter = 0

        if anomaly_counter >= MAX_ANOMALY_COUNT:
            cmd_sock.sendto(b"/SHUTDOWN", (UDP_IP, COMMAND_PORT))
            print("[!!!] EMİR GÖNDERİLDİ: SİSTEM KAPATILIYOR!")
            anomaly_counter = 0 

    except (BlockingIOError, json.JSONDecodeError):
        pass

    ax.clear()
    ax.plot(voltages, color='#00ffcc', linewidth=2)
    ax.axhline(y=ANOMALY_THRESHOLD, color='r', linestyle='--', label="Eşik")
    ax.set_ylim(200, 260) 
    ax.set_title(f"Aegis Live Control - {voltages[-1]:.2f}V")
    ax.grid(True, alpha=0.2)

ani = FuncAnimation(fig, update, interval=100)
plt.style.use('dark_background')
plt.show()