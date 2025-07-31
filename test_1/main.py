# main.py (versión avanzada para demo profesional Streamlit)

import streamlit as st
import pandas as pd
from scripts.load_data import cargar_datos_fisicos, cargar_etiquetas_tacticas
from scripts.merge_datasets import fusionar_datos_con_acciones
from scripts.analytics import (
    calcular_metricas_avanzadas,
    calcular_tasa_exito_por_jugador,
    detectar_combinaciones,
    detectar_fatiga,
    resumen_fisico_vs_resultado
)
from scripts.visualizations import (
    radar_jugador,
    mapa_calor_zonas,
    comparativa_equipo,
    dispersion_resultados,
    dispersion_ofensivo_defensivo,
    obtener_correlaciones_roles,
    curvas_fatiga
)

st.set_page_config(page_title="Mapa de Rendimiento Táctico", layout="wide")
st.title("📊 Mapa de Rendimiento Táctico – Selección Española Masculina")

# --- Cargar datos ---
df_fisicos = cargar_datos_fisicos()
df_etiquetas = cargar_etiquetas_tacticas()
df_merged = fusionar_datos_con_acciones(df_fisicos, df_etiquetas)

# --- Calcular métricas avanzadas ---
df_metricas = calcular_metricas_avanzadas(df_merged)
tasa_exito_df = calcular_tasa_exito_por_jugador(df_etiquetas)
combos_df = detectar_combinaciones(df_etiquetas)
fatiga_df = detectar_fatiga(df_fisicos)
resumen_resultados = resumen_fisico_vs_resultado(df_merged)

# --- Sidebar de control ---
st.sidebar.header("🎯 Opciones de Análisis")
jugador_sel = st.sidebar.selectbox("👤 Selecciona jugador", df_metricas["jugador"].unique())
accion_sel = st.sidebar.selectbox("⚔️ Acción táctica", df_metricas["accion"].dropna().unique())

# --- Visualizaciones principales ---
st.subheader(f"🔍 Análisis individual de {jugador_sel}")
col1, col2 = st.columns(2)
with col1:
    radar_jugador(df_metricas, jugador_sel)
with col2:
    mapa_calor_zonas(df_metricas, jugador_sel)

st.markdown("---")
comparativa_equipo(df_metricas, accion_sel)

# --- Análisis avanzado ---
st.markdown("## 🧠 Análisis Avanzado")

# Dispersión en cancha por resultado
tipo_opt = st.radio("Filtrar acciones mostradas", ["Todas", "Ofensivas", "Defensivas"], index=0)
tipo_filtro = None
if tipo_opt == "Ofensivas":
    tipo_filtro = "ataque"
elif tipo_opt == "Defensivas":
    tipo_filtro = "defensa"
dispersion_resultados(df_merged, tipo_filtro)

# Eficiencia ofensiva vs defensiva
st.markdown("### 🎯 Tasa de Éxito Ofensivo vs Defensivo")
posiciones = df_fisicos[["jugador", "posicion"]].drop_duplicates()
df_tasas_plot = tasa_exito_df.merge(posiciones, on="jugador")
dispersion_ofensivo_defensivo(df_tasas_plot)

# Correlación táctica por jugador
st.markdown("### 🧬 Correlación de Perfiles Tácticos")
fig_corr_of, fig_corr_def = obtener_correlaciones_roles(df_etiquetas)
colA, colB = st.columns(2)
with colA:
    st.plotly_chart(fig_corr_of)
with colB:
    st.plotly_chart(fig_corr_def)

# Combinaciones tácticas
st.markdown("### 🔁 Jugadas Combinadas Detectadas")
if not combos_df.empty:
    st.dataframe(combos_df)
else:
    st.info("No se detectaron jugadas combinadas relevantes.")

# Fatiga física y curvas
st.markdown("### 💥 Curvas de Fatiga y Carga")
fatiga_jugadores = fatiga_df[fatiga_df["fatiga"] == True]["jugador"].tolist()
if fatiga_jugadores:
    st.warning(f"Jugadores con signos de fatiga detectada: {', '.join(fatiga_jugadores)}")
else:
    st.success("Ningún jugador mostró fatiga significativa en la sesión.")

curvas_fatiga(df_fisicos, jugador_sel)

# Resumen físico por resultado
tabla_resumen = resumen_resultados.style.background_gradient(cmap="RdYlGn", axis=0)
st.markdown("### 📊 Comparativa Física según Resultado de Acción")
st.dataframe(tabla_resumen)

st.markdown("---")
st.caption("Prototipo desarrollado por AI Engineer – MVP táctico-físico para FEB 🏀")