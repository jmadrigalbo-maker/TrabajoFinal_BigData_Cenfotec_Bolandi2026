import json
import sys
from datetime import datetime
from kafka import KafkaConsumer
from pymongo import MongoClient

print("🔍 Conectando con MongoDB y Kafka...")

# 1. Conexión a MongoDB
try:
    mongo_client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
    db = mongo_client['twitter_db']
    collection = db['raw_comments']
    print("✅ Conectado a MongoDB")
except Exception as e:
    print(f"❌ Error al conectar a MongoDB: {e}")
    sys.exit(1)

# 2. Conexión a Kafka
try:
    consumer = KafkaConsumer(
        'twitter_comments',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='grupo_twitter_final',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    print("✅ Conectado a Kafka. Esperando mensajes...")
except Exception as e:
    print(f"❌ Error al conectar a Kafka: {e}")
    sys.exit(1)

# 3. Bucle de escucha
try:
    for message in consumer:
        comment_data = message.value
        comment_data['received_at'] = datetime.utcnow().isoformat()
        comment_data['processed'] = False
        
        inserted_id = collection.insert_one(comment_data).inserted_id
        print(f"[CONSUMER] Guardado en MongoDB | ID: {inserted_id} | Tweet: {comment_data['comment'][:50]}...")

except KeyboardInterrupt:
    print("\n🛑 Consumer detenido.")
    mongo_client.close()