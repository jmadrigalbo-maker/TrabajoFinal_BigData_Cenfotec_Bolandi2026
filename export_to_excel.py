import os
import pandas as pd
import pymysql

print("📊 Conectando a MySQL para exportar los datos...")

# 1. Conexión a MySQL
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='rootpassword',
    database='twitter_analytics',
)

# 2. Leer la tabla de MySQL
query = "SELECT id, user_id, tweet_text, sentiment, confidence_score, processed_at FROM processed_tweets"
df = pd.read_sql(query, conn)
conn.close()

# 3. Configurar la ruta automática para guardar el Excel dentro de la carpeta 'reportes'
script_dir = os.path.dirname(os.path.abspath(__file__))  # Ruta de la carpeta 'scripts'
project_root = os.path.dirname(script_dir)               # Ruta principal del proyecto
reportes_dir = os.path.join(project_root, 'reportes')

os.makedirs(reportes_dir, exist_ok=True)
excel_path = os.path.join(reportes_dir, 'tweets_procesados.xlsx')

# 4. Guardar en archivo Excel
df.to_excel(excel_path, index=False, engine='openpyxl')

print(f"✅ ¡Éxito! Se exportaron {len(df)} tweets a la hoja de Excel.")
print(f"📁 Ubicación del archivo: {os.path.abspath(excel_path)}")