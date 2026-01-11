import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

db_path = os.path.join('data', 'aegis_records.db')
model_dir = "models"
model_path = os.path.join(model_dir, "aegis_brain.pkl")

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT voltage, current, is_anomaly FROM telemetry", conn)
conn.close()

if len(df) < 50:
    print(f"Yetersiz veri: {len(df)}/50. Lütfen C++ tarafini biraz daha calistirin.")
else:
    X = df[['voltage', 'current']]
    y = df['is_anomaly']

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    joblib.dump(model, model_path)
    
    if os.path.exists(model_path):
        print(f"Aegis-Brain olusturuldu: {model_path}")
        print(f"Veri seti boyutu: {len(df)}")