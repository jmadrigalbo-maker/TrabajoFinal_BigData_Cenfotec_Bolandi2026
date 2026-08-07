# 📊 Sistema de Análisis de Sentimiento en Tiempo Real (Big Data)

Este proyecto es una arquitectura end-to-end en streaming para la ingesta, almacenamiento, procesamiento con IA y visualización interactiva en tiempo real de tweets y opiniones de usuarios.

---

## Arquitectura del Sistema

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

### Instalacion desde gitbub
Abrie en la terminal el siguiente codigo

git clone https://github.com/TU_USUARIO/TrabajoFinal_BigData_Cenfotec_Bolandi2026.git

# Luego entrar a la carpeta ejecutando

cd TrabajoFinal_BigData_Cenfotec_Bolandi2026

Luego seguir pasos de instalacion

### Instalacion desde el ZIP empezar desde aca.
## Para hacer paso 1 y 2 a la vez ejecutar

docker compose -f docker/docker-compose.yml up -d && python3 -m venv venv_prueba && source venv_prueba/bin/activate && pip install -r requirements.txt


### 1. Levantar la Infraestructura (Docker)
 Docker Desktop iniciado  y ejecutando

cd docker
docker compose up -d


### 2. Preparar el Entorno de Python e Instalar Dependencias

# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno (Mac/Linux)
source venv/bin/activate

# Instalar librerías
pip install -r requirements.txt

### 3. Ejecución del Pipeline 
Abrir  4 terminales independientes en VS Code, activar el entorno (source ../venv/bin/activate) en cada una y ejecutr

- Terminal 1 (Cliente/productor):
  cd scripts
  python cliente.py

- Terminal 2 (Consumer):
  cd scripts
  python consumer.py

- Terminal 3 (Procesador IA):
  cd scripts
  python processor.py

- Terminal 4 (Dashboard de Monitoreo):
  cd scripts
  streamlit run dashboard.py

---

## 🛠️ Herramientas de Utilidad

- Reiniciar la base de datos a cero 

  cd scripts
  python reset_db.py

- Exportar los datos analizados a un reporte de Excel:

  cd scripts
  python export_to_excel.py

  

  
