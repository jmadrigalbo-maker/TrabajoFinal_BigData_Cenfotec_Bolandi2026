
'''
import time
from pymongo import MongoClient
import pymysql
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1. Conexión a MongoDB (Data Lake - Datos Crudos)
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['twitter_db']
raw_collection = mongo_db['raw_comments']

# 2. Configuración de MySQL (se elimina 'database' para conectar al servidor general)
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rootpassword'
}

# 3. Cargar Modelo de Deep Learning desde Hugging Face usando PyTorch directamente
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
print("🧠 Cargando modelo de Deep Learning (PyTorch + Hugging Face)...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

LABELS = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']

def analyze_sentiment(text):
    """Procesa el texto a través de PyTorch y retorna el sentimiento y su score de confianza"""
    if not text or text.strip() == "":
        return 'NEUTRAL', 0.0

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]

    predicted_class = torch.argmax(probabilities).item()
    sentiment = LABELS[predicted_class]
    confidence = round(probabilities[predicted_class].item(), 4)

    return sentiment, confidence

print("🤖 Procesador con PyTorch e IA iniciado. Buscando tweets no procesados...")

try:
    mysql_conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = mysql_conn.cursor()

    # -------------------------------------------------------------------------
    # 🛠️ INICIALIZACIÓN AUTOMÁTICA: Crear Base de Datos y Tabla si no existen
    # -------------------------------------------------------------------------
    cursor.execute("CREATE DATABASE IF NOT EXISTS twitter_analytics;")
    cursor.execute("USE twitter_analytics;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_tweets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(50),
            tweet_text TEXT NOT NULL,
            sentiment VARCHAR(20) NOT NULL,
            confidence_score FLOAT,
            processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    mysql_conn.commit()
    print("✅ Base de datos 'twitter_analytics' y tabla 'processed_tweets' verificadas/creadas.")
    # -------------------------------------------------------------------------

    while True:
        # Verificar que la conexión a MySQL siga viva antes de procesar
        mysql_conn.ping(reconnect=True)

        unprocessed_tweets = list(raw_collection.find({'processed': False}).limit(10))

        if not unprocessed_tweets:
            time.sleep(2)
            continue

        for tweet in unprocessed_tweets:
            tweet_id = tweet['_id']
            user_id = tweet.get('user_id', 'unknown')
            comment_text = tweet.get('comment', '')

            # Inferencia con PyTorch
            sentiment, score = analyze_sentiment(comment_text)

            # Guardar en MySQL
            sql = """
                INSERT INTO processed_tweets (user_id, tweet_text, sentiment, confidence_score)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, comment_text, sentiment, score))
            mysql_conn.commit()

            # Marcar como procesado en MongoDB
            raw_collection.update_one(
                {'_id': tweet_id},
                {'$set': {'processed': True}}
            )

            print(f"✅ [PyTorch ML] ID: {tweet_id} | Sentimiento: {sentiment} ({score}) | Tweet: {comment_text[:40]}...")

except KeyboardInterrupt:
    print("\n🛑 Procesador detenido por el usuario.")
    if 'mysql_conn' in locals() and mysql_conn.open:
        cursor.close()
        mysql_conn.close()
    mongo_client.close()
except Exception as e:
    print(f"❌ Error en el procesador: {e}")


    '''




import time
from pymongo import MongoClient
import pymysql
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1. Conexión a MongoDB (Data Lake - Datos Crudos)
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['twitter_db']
raw_collection = mongo_db['raw_comments']

# 2. Configuración de MySQL
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rootpassword'
}

# 3. Cargar el NUEVO Modelo Multilingüe desde Hugging Face
MODEL_NAME = "tabularisai/multilingual-sentiment-analysis"
print("🧠 Cargando modelo Multilingüe de Deep Learning (PyTorch + Hugging Face)...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

# NUEVAS ETIQUETAS (El modelo nuevo clasifica en 5 clases de 0 a 4)
SENTIMENT_MAP = {
    0: "Very Negative", 
    1: "Negative", 
    2: "Neutral", 
    3: "Positive", 
    4: "Very Positive"
}

def analyze_sentiment(text):
    """Procesa el texto con el nuevo modelo multilingüe y retorna sentimiento y confianza"""
    if not text or text.strip() == "":
        return 'Neutral', 0.0

    # Tokenizado para el nuevo modelo
    inputs = tokenizer([text], return_tensors="pt", truncation=True, padding=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]

    predicted_class = torch.argmax(probabilities).item()
    sentiment = SENTIMENT_MAP[predicted_class]
    confidence = round(probabilities[predicted_class].item(), 4)

    return sentiment, confidence

print("🤖 Procesador Multilingüe con PyTorch e IA iniciado. Buscando tweets no procesados...")

try:
    mysql_conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = mysql_conn.cursor()

    # -------------------------------------------------------------------------
    # 🛠️ INICIALIZACIÓN AUTOMÁTICA: Crear Base de Datos y Tabla si no existen
    # -------------------------------------------------------------------------
    cursor.execute("CREATE DATABASE IF NOT EXISTS twitter_analytics;")
    cursor.execute("USE twitter_analytics;")
    
    # NOTA: En MySQL, 'sentiment VARCHAR(20)' almacenará sin problemas valores 
    # más largos como "Very Negative" o "Very Positive".
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_tweets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(50),
            tweet_text TEXT NOT NULL,
            sentiment VARCHAR(20) NOT NULL,
            confidence_score FLOAT,
            processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    mysql_conn.commit()
    print("✅ Base de datos 'twitter_analytics' y tabla 'processed_tweets' verificadas/creadas.")
    # -------------------------------------------------------------------------

    while True:
        # Verificar que la conexión a MySQL siga viva antes de procesar
        mysql_conn.ping(reconnect=True)

        unprocessed_tweets = list(raw_collection.find({'processed': False}).limit(10))

        if not unprocessed_tweets:
            time.sleep(2)
            continue

        for tweet in unprocessed_tweets:
            tweet_id = tweet['_id']
            user_id = tweet.get('user_id', 'unknown')
            comment_text = tweet.get('comment', '')

            # Inferencia con la nueva función
            sentiment, score = analyze_sentiment(comment_text)

            # Guardar en MySQL
            sql = """
                INSERT INTO processed_tweets (user_id, tweet_text, sentiment, confidence_score)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, comment_text, sentiment, score))
            mysql_conn.commit()

            # Marcar como procesado en MongoDB
            raw_collection.update_one(
                {'_id': tweet_id},
                {'$set': {'processed': True}}
            )

            print(f"✅ [Multilingual ML] ID: {tweet_id} | Sentimiento: {sentiment} ({score}) | Tweet: {comment_text[:40]}...")

except KeyboardInterrupt:
    print("\n🛑 Procesador detenido por el usuario.")
    if 'mysql_conn' in locals() and mysql_conn.open:
        cursor.close()
        mysql_conn.close()
    mongo_client.close()
except Exception as e:
    print(f"❌ Error en el procesador: {e}")


    