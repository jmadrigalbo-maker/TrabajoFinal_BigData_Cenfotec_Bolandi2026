
import pandas as pd
import plotly.express as px
import pymysql
import streamlit as st

st.set_page_config(page_title="Twitter Sentiment Dashboard", layout="wide")

st.title("📊 Dashboard de Análisis de Sentimiento en Tiempo Real")
st.markdown("Procesamiento de Big Data con Kafka, MongoDB, MySQL y NLP Multilingüe")


def load_data():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="rootpassword",
        database="twitter_analytics",
    )
    df = pd.read_sql_query("SELECT * FROM processed_tweets", conn)
    conn.close()
    return df


@st.fragment(run_every="3s")
def render_dashboard():
    df = load_data()

    # Métricas adaptadas a las 5 clases o agrupadas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Total Tweets", len(df))
    
    # Conteo de Positivos (Muy Positivo + Positivo)
    positivos = len(df[df["sentiment"].isin(["Positive", "Very Positive"])])
    col2.metric("Positivos", positivos)
    
    # Conteo de Neutrales
    neutrales = len(df[df["sentiment"] == "Neutral"])
    col3.metric("Neutrales", neutrales)
    
    # Conteo de Negativos (Muy Negativo + Negativo)
    negativos = len(df[df["sentiment"].isin(["Negative", "Very Negative"])])
    col4.metric("Negativos", negativos)
    
    # Confianza Promedio General
    avg_conf = round(df["confidence_score"].mean(), 2) if not df.empty else 0.0
    col5.metric("Confianza Media", f"{avg_conf}")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Distribución de Sentimientos (5 Niveles)")
        # Gráfico circular con paleta de colores coherente
        color_discrete_map = {
            "Very Positive": "#1b5e20",
            "Positive": "#4caf50",
            "Neutral": "#ffeb3b",
            "Negative": "#f44336",
            "Very Negative": "#b71c1c"
        }
        fig = px.pie(
            df, 
            names="sentiment", 
            title="Proporción de Sentimientos", 
            hole=0.4,
            color="sentiment",
            color_discrete_map=color_discrete_map
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Confianza Media del Modelo")
        fig2 = px.histogram(
            df,
            x="confidence_score",
            color="sentiment",
            title="Distribución del Score de Confianza por Sentimiento",
            color_discrete_map=color_discrete_map
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Lectura directa de Tweets Procesados")
    st.dataframe(
        df.sort_values(by="id", ascending=False), use_container_width=True
    )


render_dashboard()