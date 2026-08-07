import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='rootpassword',
    database='twitter_analytics'
)

cursor = conn.cursor()

# 1. Total de tweets procesados
cursor.execute("SELECT COUNT(*) FROM processed_tweets;")
total = cursor.fetchone()[0]

# 2. Resumen por sentimiento
cursor.execute("""
    SELECT sentiment, COUNT(*) 
    FROM processed_tweets 
    GROUP BY sentiment;
""")
resumen = cursor.fetchall()

print(f"📊 TOTAL DE TWEETS ANALIZADOS EN MYSQL: {total}\n")
print("📈 DISTRIBUCIÓN DE SENTIMIENTOS:")
for fila in resumen:
    print(f"  • {fila[0]}: {fila[1]}")

# 3. Mostrar los últimos 5
cursor.execute("SELECT tweet_text, sentiment, confidence_score FROM processed_tweets ORDER BY id DESC LIMIT 5;")
ultimos = cursor.fetchall()

print("\n🔍 ÚLTIMOS 5 TWEETS PROCESADOS:")
for tweet, sent, score in ultimos:
    print(f"  [{sent}] (score: {score}) -> {tweet[:70]}...")

cursor.close()
conn.close()