# visualizations.py (mejorado al nivel máximo)

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# 1. Radar por tipo de acción

def radar_jugador(df_metricas, jugador):
    df = df_metricas[df_metricas["jugador"] == jugador]
    df_radar = df.groupby("accion")["playerload_mean"].mean().reset_index()
    fig = px.line_polar(df_radar, r="playerload_mean", theta="accion", line_close=True,
                        title=f"Carga física por acción – {jugador}")
    st.plotly_chart(fig)

# 2. Mapa de calor en pista con coordenadas reales

def mapa_calor_zonas(df_metricas, jugador):
    df = df_metricas[df_metricas["jugador"] == jugador]
    fig = px.density_heatmap(
        df, x="x_pos_mean", y="y_pos_mean", z="playerload_mean",
        nbinsx=14, nbinsy=7, color_continuous_scale="Hot",
        title=f"Mapa de Carga Física - {jugador}", labels={"x_pos_mean": "Ancho cancha (m)", "y_pos_mean": "Largo cancha (m)"}
    )
    fig.update_layout(yaxis_scaleanchor="x", xaxis_range=[0, 28], yaxis_range=[0, 15])
    st.plotly_chart(fig)

# 3. Comparativa de carga por acción en equipo

def comparativa_equipo(df_metricas, accion):
    df_accion = df_metricas[df_metricas["accion"] == accion]
    df_bar = df_accion.groupby("jugador")["playerload_mean"].mean().reset_index()
    fig = px.bar(df_bar, x="jugador", y="playerload_mean", title=f"Carga Media – Acción: {accion}", color="playerload_mean",
                 color_continuous_scale="Blues")
    st.plotly_chart(fig)

# 4. Dispersión por zona + resultado + carga

def dispersion_resultados(df, tipo_filtro=None):
    df_plot = df if tipo_filtro is None else df[df["tipo"] == tipo_filtro]
    if df_plot.empty:
        st.warning("No hay eventos registrados para el filtro aplicado.")
        return
    fig = px.scatter(
        df_plot, x="x_pos", y="y_pos",
        color="resultado", symbol="accion", size="playerload",
        color_discrete_map={"Exito": "green", "Fallo": "red"},
        labels={"x_pos": "X (cancha)", "y_pos": "Y (cancha)"},
        title="Mapa de Acciones: Posición vs Carga y Resultado"
    )
    fig.update_layout(yaxis_scaleanchor="x", xaxis_range=[0, 28], yaxis_range=[0, 15])
    st.plotly_chart(fig)

# 5. Dispersión ofensivo vs defensivo por jugador

def dispersion_ofensivo_defensivo(df_jugadores):
    fig = px.scatter(
        df_jugadores, x="tasa_exito_ofensivo", y="tasa_exito_defensivo",
        color="posicion", text="jugador",
        title="Rendimiento Individual: Éxito Ofensivo vs Defensivo",
        labels={"tasa_exito_ofensivo": "Éxito Ofensivo", "tasa_exito_defensivo": "Éxito Defensivo"}
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig)

# 6. Correlación de perfiles de acción

def obtener_correlaciones_roles(df_etiquetas):
    of_counts = df_etiquetas[df_etiquetas["tipo"] == "ataque"].groupby(["jugador", "accion"]).size().unstack(fill_value=0)
    def_counts = df_etiquetas[df_etiquetas["tipo"] == "defensa"].groupby(["jugador", "accion"]).size().unstack(fill_value=0)
    corr_of = of_counts.T.corr()
    corr_def = def_counts.T.corr()
    fig_of = px.imshow(corr_of, text_auto=True, title="Correlación Ofensiva entre Jugadores")
    fig_def = px.imshow(corr_def, text_auto=True, title="Correlación Defensiva entre Jugadores")
    return fig_of, fig_def

# 7. Curvas HR / Carga con doble eje Y

def curvas_fatiga(df_fisicos, jugador):
    dfp = df_fisicos[df_fisicos["jugador"] == jugador]
    if dfp.empty:
        st.info("No hay datos disponibles para este jugador.")
        return
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=dfp["tiempo"], y=dfp["hr"], name="Frecuencia Cardíaca (bpm)", line=dict(color='red')), secondary_y=False)
    fig.add_trace(go.Scatter(x=dfp["tiempo"], y=dfp["playerload"], name="Carga (PlayerLoad)", line=dict(color='blue', dash='dot')), secondary_y=True)
    fig.update_layout(title=f"Curvas Fisiológicas – {jugador}", xaxis_title="Tiempo (s)")
    fig.update_yaxes(title_text="HR (bpm)", secondary_y=False)
    fig.update_yaxes(title_text="PlayerLoad", secondary_y=True)
    st.plotly_chart(fig)

# 8. Análisis de éxito físico-táctico agregado

def resumen_fisico_vs_exito(df_rendimiento):
    fig = px.bar(df_rendimiento, x="tipo_resultado", y=["playerload", "velocidad", "hr"], barmode="group",
                 title="Comparativa Física – Éxito vs Fallo",
                 labels={"value": "Promedio", "variable": "Métrica"})
    st.plotly_chart(fig)
