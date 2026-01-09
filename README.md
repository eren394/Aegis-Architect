#  Aegis Architect: Industrial IoT Monitoring & Anomaly Detection

Aegis Architect is a high-performance, real-time industrial monitoring system. It features a **C++ Core** for high-speed data emission and a **Python Mind** for real-time data visualization, logging, and predictive anomaly detection.

##  Features
- **High-Speed Data Emission:** C++ backend simulating industrial sensor data (Voltage & Flow).
- **Real-Time Visualization:** Python-based dashboard using Matplotlib for live telemetry.
- **Persistent Logging:** Automatic JSON-based data logging for future AI/ML training.
- **Anomaly Detection:** Smart algorithm that detects voltage surges and prevents system failures.
- **Cross-Platform Communication:** Robust UDP socket implementation between C++ and Python.

##  Tech Stack
- **Backend:** C++ (WinSock2, TCP/IP, UDP)
- **Analytics & UI:** Python (Matplotlib, Sockets, JSON)
- **Data Format:** JSON

##  Project Structure
- `/core`: C++ Source files (The Emitter)
- `/brain`: Python scripts (The Analyzer)
- `/data`: Persistent storage for system logs

##  How to Run
1. Run the Python Analyzer: `python brain/analyzer.py`
2. Run the C++ Core: `./aegis_core.exe`

