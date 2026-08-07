import time
import json
import random
import pandas as pd
import glob
import os
import kagglehub
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("📥 [CLIENTE 1] Cargando dataset...")
path = kagglehub.dataset_download("durgeshrao9993/twitter-analysis-dataset-2022")
csv_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.read_csv(csv_files[0])

columna_texto = next((col for col in df.columns if col.lower() in ['text', 'tweet', 'comment', 'content', 'tweets']), df.columns[0])

print(f"🚀 [CLIENTE 1] Iniciado. Enviando tweets...")

try:
    for index, row in df.iloc[::2].iterrows(): # Toma las filas pares
        comment_text = str(row[columna_texto])
        if not comment_text or comment_text.strip() == "" or comment_text == "nan":
            continue

        mensaje = {
            "user_id": f"user_c1_{random.randint(100, 499)}",
            "comment": comment_text
        }
        
        producer.send('twitter_comments', value=mensaje)
        producer.flush()
        
        # CADENCIA ALEATORIA ENTRE 0.5 Y 3 SEGUNDOS
        delay = round(random.uniform(0.5, 3.0), 2)
        print(f"🟢 [CLIENTE 1] Fila {index} enviada (Espera: {delay}s) | {comment_text[:40]}...")
        time.sleep(delay)

except KeyboardInterrupt:
    print("\n🛑 [CLIENTE 1] Detenido.")
    producer.close()