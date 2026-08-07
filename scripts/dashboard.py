import pandas as pd
import plotly.express as px
import pymysql
import streamlit as st

st.set_page_config(page_title="Twitter Sentiment Dashboard", layout="wide")

st.title("📊 Dashboard de Análisis de Sentimiento en Tiempo Real")
st.markdown("Procesamiento de Big Data con Kafka, MongoDB, MySQL y NLP")


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

  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Total Tweets", len(df))
  col2.metric(
      "Positivos", len(df[df["sentiment"] == "POSITIVE"]), delta_color="normal"
  )
  col3.metric(
      "Negativos", len(df[df["sentiment"] == "NEGATIVE"]), delta_color="inverse"
  )
  col4.metric("Neutrales", len(df[df["sentiment"] == "NEUTRAL"]))

  st.divider()

  c1, c2 = st.columns(2)

  with c1:
    st.subheader("Distribución de Sentimientos")
    fig = px.pie(
        df, names="sentiment", title="Proporción de Sentimientos", hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

  with c2:
    st.subheader("Confianza Media del Modelo")
    fig2 = px.histogram(
        df,
        x="confidence_score",
        color="sentiment",
        title="Distribución del Score de Polaridad",
    )
    st.plotly_chart(fig2, use_container_width=True)

  st.subheader("📋 Lectura directa de Tweets Procesados")
  st.dataframe(
      df.sort_values(by="id", ascending=False), use_container_width=True
  )


render_dashboard()
