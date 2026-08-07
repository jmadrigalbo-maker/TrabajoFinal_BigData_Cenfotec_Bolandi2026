from pymongo import MongoClient
import pymysql

print("🧹 Limpiando bases de datos para reiniciar conteo...")

# 1. Limpiar MongoDB (Data Lake)
try:
  mongo_client = MongoClient('mongodb://localhost:27017/')
  mongo_db = mongo_client['twitter_db']
  mongo_db['raw_comments'].delete_many({})
  print("✅ MongoDB limpiado (0 documentos).")
except Exception as e:
  print(f"❌ Error al limpiar MongoDB: {e}")

# 2. Limpiar MySQL (Data Warehouse)
try:
  conn = pymysql.connect(
      host='localhost',
      port=3306,
      user='root',
      password='rootpassword',
      database='twitter_analytics',
  )
  cursor = conn.cursor()
  cursor.execute('TRUNCATE TABLE processed_tweets;')
  conn.commit()
  cursor.close()
  conn.close()
  print("✅ MySQL limpiado (Tabla resetear a ID 1).")
except Exception as e:
  print(f"❌ Error al limpiar MySQL: {e}")

print("✨ ¡Todo listo para iniciar un nuevo conteo desde cero!")