import time
import json
import random
import pandas as pd
import glob
import os
import kagglehub
from kafka import KafkaProducer

# 1. Configurar la conexión a Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("📥 Descargando/Cargando dataset desde Kaggle...")
path = kagglehub.dataset_download("durgeshrao9993/twitter-analysis-dataset-2022")

csv_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.read_csv(csv_files[0])

columna_texto = None
for col in df.columns:
    if col.lower() in ['text', 'tweet', 'comment', 'content', 'tweets']:
        columna_texto = col
        break
if not columna_texto:
    columna_texto = df.columns[0]

print(f"🚀 Producer listo. Enviando datos de '{columna_texto}' a Kafka...")

try:
    for index, row in df.iterrows():
        comment_text = str(row[columna_texto])
        if not comment_text or comment_text.strip() == "" or comment_text == "nan":
            continue

        mensaje = {
            "user_id": f"user_{random.randint(100, 999)}",
            "comment": comment_text
        }
        
        producer.send('twitter_comments', value=mensaje)
        producer.flush() # Forza el envío inmediato del mensaje a Kafka
        print(f"[PRODUCER] Enviado fila {index}: {comment_text[:60]}...")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Producer detenido.")
    producer.close()