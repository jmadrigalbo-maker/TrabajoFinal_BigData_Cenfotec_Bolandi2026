import pymysql

# Configuración de conexión a MySQL (Servidor en Docker)
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rootpassword',  # Contraseña definida en docker-compose
}

print("🔌 Conectando al servidor MySQL...")

try:
  # 1. Conectar a MySQL sin especificar base de datos
  conn = pymysql.connect(**DB_CONFIG)
  cursor = conn.cursor()

  # 2. Crear la base de datos si no existe
  cursor.execute("CREATE DATABASE IF NOT EXISTS twitter_analytics;")
  cursor.execute("USE twitter_analytics;")
  print("✅ Base de datos 'twitter_analytics' lista.")

  # 3. Crear la tabla de tweets analizados
  create_table_query = """
    CREATE TABLE IF NOT EXISTS processed_tweets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(50),
        tweet_text TEXT NOT NULL,
        sentiment VARCHAR(20) NOT NULL,
        confidence_score FLOAT,
        processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
  cursor.execute(create_table_query)
  conn.commit()

  print("✅ Tabla 'processed_tweets' creada correctamente en MySQL.")

  cursor.close()
  conn.close()

except Exception as e:
  print(f"❌ Error al configurar MySQL: {e}")
  print(
      "👉 Revisa que el contenedor de MySQL en Docker esté iniciado y corriendo"
      " en el puerto 3306."
  )
  