# Sistema de Análisis de Sentimiento en Tiempo Real

Este proyecto implementa una arquitectura para captar, almacenar, procesar con Inteligencia Artificial (Procesamiento del Lenguaje Natural) y visualización de dashboard en tiempo real de tweets y opiniones de usuarios.

---

##  Arquitectura del Sistema

- **Produccion y Mensajería:** Apache Kafka (Producer / Consumer)
- **Data Lake:** MongoDB
- **Data Warehouse (Datos Procesados):** MySQL
- **Procesamiento IA Deep learning:** Python (PyTorch + Hugging Face RoBERTa)
- **Visualización Analítica:** - Visualización Analítica: Metabase (Dashboard BI principal) + Streamlit (Monitoreo auxiliar)

---

## Estructura del Proyecto

proyectoFinal-bigdata-twitter/
├── docker/
│   └── docker-compose.yml       # Contenedores de Kafka, MongoDB y MySQL
├── scripts/
│   ├── cliente1.py               # Producer (Descarga dataset e ingiere a Kafka)
│   ├── cliente2.py               # Producer (Descarga dataset e ingiere a Kafka)
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

##  Guía de Instalación y Ejecución

# ***Desde github****
ejecutar esto en la terminal

git clone https://github.com/jmadrigalbo-maker/TrabajoFinal_BigData_Cenfotec_Bolandi2026

cd TrabajoFinal_BigData_Cenfotec_Bolandi2026


# ***DEsde el ZIP**

# *Para compactar Paso 1 y 2 ejecutar
docker compose -f docker/docker-compose.yml up -d && python3 -m venv venv_prueba && source venv_prueba/bin/activate && pip install -r requirements.txt

### 1. Levantar la Infraestructura (Docker)
Tener Docker Desktop ejecutandos, ejecutar en la terminal.

docker compose up -d

### 2. Preparar el Entorno de Python e Instalar Dependencias

# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno (Mac/Linux)
source venv/bin/activate

# Instalar librerías
pip install -r requirements.txt

### 3. Ejecución del Pipeline 
Abrir 5 terminales independientes en VS Code, activando siempre el entorno (source venv/bin/activate) en cada una y ejecutando los siguientes comandos en orden:

- Terminal 1 (Producer /cliente):

python scripts/cliente1.py 

  - Terminal 2 (Producer /cliente):

python scripts/cliente2.py 


- Terminal 3 (Consumer / Data Lake):
 
  python scripts/consumer.py

- Terminal 4 (Procesador IA / Data Warehouse):

  python scripts/processor.py

- Terminal 5 (Dashboard de Monitoreo):

  streamlit run scripts/dashboard.py


### 📊 Acceso a Dashboards
- **Metabase (Principal):** Abrir en el navegador `http://localhost:3000`
- **Streamlit (Auxiliar):** Se ejecuta desde la Terminal 5 (`http://localhost:8501`)
---

## 🛠️ Herramientas de Utilidad

- Reiniciar la base de datos a cero (Limpieza antes de una prueba):

  python scripts/reset_db.py

- Exportar los datos analizados a un reporte de Excel:

  python scripts/export_to_excel.py

  

  
