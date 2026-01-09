import socket
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sqlite3
import os

if not os.path.exists('data'):
    os.makedirs('data')

db_conn = sqlite3.connect('data/aegis_records.db', check_same_thread=False)
cursor = db_conn.cursor()
cursor.execute("DROP TABLE IF EXISTS telemetry") 
cursor.execute('''
    CREATE TABLE telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT (DATETIME('now', 'localtime')),
        voltage REAL,
        current REAL,
        is_anomaly INTEGER
    )
''')
db_conn.commit()

def save_to_db(v, c, anomaly):
    try:
        cursor.execute("INSERT INTO telemetry (voltage, current, is_anomaly) VALUES (?, ?, ?)", 
                       (v, c, 1 if anomaly else 0))
        db_conn.commit() 
    except Exception as e:
        print(f"DB Hatası: {e}")

UDP_IP = "127.0.0.1"
UDP_PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

fig, ax = plt.subplots()
voltages, currents = [0], [0] 

def update(frame):
    
    try:
        data, addr = sock.recvfrom(1024)
        print(f"BULDUM! Veri geldi: {data.decode()}")
        msg = json.loads(data.decode())
        
        v = msg["voltage"]
        c = msg["current"]
        is_anom = v > 15.0 
        
        voltages.append(v)
        currents.append(c)
        save_to_db(v, c, is_anom)
        
        ax.cla()
        ax.plot(voltages[-30:], color='#00ffcc', linewidth=2, label=f"Voltage: {v:.2f}V")
        ax.axhline(y=15, color='r', linestyle='--', label="Limit (15V)")
        ax.set_ylim(0, 25) 
        ax.legend(loc='upper left')
        ax.set_facecolor('#222222') 
        
        if is_anom:
            ax.set_title("⚠️ AEGIS ALERT: ANOMALY DETECTED! ⚠️", color='red', fontweight='bold')
        else:
            ax.set_title("Aegis Architect - Live Resource Monitoring", color='white')
            
    except (BlockingIOError, json.JSONDecodeError):
        pass

ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
plt.style.use('dark_background') 
plt.show()