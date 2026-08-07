# 📊 Sistema de Análisis de Sentimiento en Tiempo Real (Big Data)

Este proyecto implementa una arquitectura end-to-end en streaming para la ingesta, almacenamiento, procesamiento con Inteligencia Artificial (Procesamiento del Lenguaje Natural) y visualización interactiva en tiempo real de tweets y opiniones de usuarios.

---

## 🏗️ Arquitectura del Sistema

- **Ingesta y Mensajería:** Apache Kafka (Producer / Consumer)
- **Data Lake (Datos Crudos):** MongoDB
- **Data Warehouse (Datos Procesados):** MySQL
- **Procesamiento e IA:** Python (TextBlob / Transformers)
- **Visualización Analítica:** Dashboard interactivo en Streamlit

---

## 📂 Estructura del Proyecto

proyectoFinal-bigdata-twitter/
├── docker/
│   └── docker-compose.yml       # Contenedores de Kafka, MongoDB y MySQL
├── scripts/
│   ├── cliente.py               # Producer (Descarga dataset e ingiere a Kafka)
│   ├── consumer.py              # Consumer (Almacena datos crudos en MongoDB)
│   ├── processor.py             # Procesador IA (Analiza sentimientos y guarda en MySQL)
│   ├── dashboard.py             # Dashboard analítico interactivo
│   ├── export_to_excel.py       # Herramienta para exportar datos a Excel
│   └── reset_db.py              # Script para reiniciar tablas y colecciones a cero
├── reportes/
│   └── tweets_procesados.xlsx   # Reporte consolidado generado
├── Informe_Tecnico_Proyecto_BigData.pdf # Documentación técnica formal
├── requirements.txt             # Librerías y dependencias de Python
└── README.md                    # Guía de uso e instalación

---

## 🚀 Guía de Instalación y Ejecución

### 1. Levantar la Infraestructura (Docker)
Asegúrate de tener Docker Desktop iniciado y ejecuta:

cd docker
docker compose up -d

(Espera unos 10-15 segundos mientras se inician Kafka, MongoDB y MySQL).

### 2. Preparar el Entorno de Python e Instalar Dependencias

# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno (Mac/Linux)
source venv/bin/activate

# Activar el entorno (Windows - PowerShell)
# .\venv\Scripts\activate

# Instalar librerías
pip install -r requirements.txt

### 3. Ejecución del Pipeline en Tiempo Real
Abre 4 terminales independientes en VS Code, activa el entorno (source ../venv/bin/activate) en cada una y ejecuta los siguientes comandos en orden:

- Terminal 1 (Producer / Ingesta):
  cd scripts
  python cliente.py

- Terminal 2 (Consumer / Data Lake):
  cd scripts
  python consumer.py

- Terminal 3 (Procesador IA / Data Warehouse):
  cd scripts
  python processor.py

- Terminal 4 (Dashboard de Monitoreo):
  cd scripts
  streamlit run dashboard.py

---

## 🛠️ Herramientas de Utilidad

- Reiniciar la base de datos a cero (Limpieza antes de una prueba):
  cd scripts
  python reset_db.py

- Exportar los datos analizados a un reporte de Excel:
  cd scripts
  python export_to_excel.py

  

  