#  Aegis Architect: AI-Powered Industrial Control & Monitoring

Aegis Architect is a high-performance, real-time industrial monitoring and security system. It features a **C++ Core** for high-speed telemetry and a **Python Intelligence Layer** that provides real-time web visualization, SQLite persistence, and predictive anomaly detection with an automated "Kill Switch" mechanism.

---

##  Key Features

* **High-Speed Emitter (C++):** Simulates industrial sensor data (Voltage & Current) with low-latency UDP broadcasting.
* **AI Intelligence (Python):** Uses Scikit-Learn trained models to predict anomalies in real-time based on historical power surge patterns.
* **Web Dashboard:** A responsive, dark-themed Flask-SocketIO interface for live monitoring without page refreshes.
* **Automated Defense:** Integrated "Kill Switch" that sends a `/SHUTDOWN` command back to the C++ core upon anomaly detection.
* **Reliable Logging:** Persistent data storage using SQLite, ensuring all telemetry is recorded for post-incident analysis.
* **Bi-Directional Communication:** Full-duplex communication between C++ and Python using UDP protocols.

---

##  Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Core** | C++, WinSock2, UDP Sockets, `nlohmann/json` |
| **Intelligence** | Python 3.12, Scikit-Learn, Joblib, Threading |
| **Web Interface** | Flask, Flask-SocketIO, Socket.io (JS) |
| **Database** | SQLite3 |
| **Theme** | Cyberpunk Dark UI |

---

##  AI Mechanism

Aegis doesn't just watch; it **thinks**. The Python "Mind" uses a pre-trained classification model to analyze every incoming packet. 
1. **Data Ingestion:** Receives voltage/current data via UDP.
2. **Inference:** AI model evaluates the risk level.
3. **Action:** If an anomaly (surge) is detected, Aegis automatically triggers a remote shutdown of the C++ Core to prevent hardware damage.

---

##  Project Structure

```text
TheArchitect/
├── aegis_app.py        # Main Python Entry (AI, Flask & SocketIO)
├── core/               # C++ Source files (The Emitter & Listener)
├── templates/          # Web Dashboard HTML
├── data/               # SQLite Database (aegis_records.db)
└── models/             # Pre-trained AI Models (aegis_brain.pkl)

##  How to Run
1. Requirements

    MSYS2 (UCRT64) with GCC/G++

    Python 3.12+

    Required Python Packages:
    Bash

    pip install flask flask-socketio scikit-learn joblib

2. Execution

    Start the Intelligence Layer:
    Bash

python aegis_app.py

Ignite the Core: Run your compiled aegis_core.exe from the terminal.

Access the Dashboard: Open your browser and navigate to http://127.0.0.1:5000
