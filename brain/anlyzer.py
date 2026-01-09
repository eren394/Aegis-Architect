import socket
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

UDP_IP = "127.0.0.1"
UDP_PORT = 6666
LOG_FILE = "data/system_logs.json"

if not os.path.exists("data"):
    os.makedirs("data")

print(f"[*] Kapı açılıyor: {UDP_IP}:{UDP_PORT}")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.5) 

voltages, flows, times = [], [], []
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

def animate(i):
    global sock
    try:
        data, addr = sock.recvfrom(1024)
        print(f"[OK] Veri geldi: {data.decode()[:20]}...") 
        
        payload = json.loads(data.decode())
        
        payload["timestamp"] = datetime.now().strftime("%H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(payload) + "\n")

        voltages.append(payload["voltage"])
        flows.append(payload["water_flow"])
        times.append(len(voltages))

        if len(voltages) > 30:
            voltages.pop(0); flows.pop(0); times.pop(0)

        ax1.clear(); ax2.clear()
        ax1.plot(times, voltages, color='lime'); ax1.set_title("Voltage")
        ax2.plot(times, flows, color='cyan'); ax2.set_title("Flow")

    except socket.timeout:
        print("[!] Bekleniyor... (Veri henüz ulaşmadı)")
    except Exception as e:
        print(f"[HATA] {e}")

ani = FuncAnimation(fig, animate, interval=500)
plt.show()