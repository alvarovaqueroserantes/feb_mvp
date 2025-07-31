# merge_datasets.py (versión mejorada con contexto colectivo y zonas GPS)

import pandas as pd
import numpy as np

def determinar_zona_gps(x, y):
    # Define zonas simplificadas de la cancha según coordenadas reales (28x15 m)
    if x < 6:
        return "esquina izquierda"
    elif x > 22:
        return "esquina derecha"
    elif 10 < x < 18 and y < 5:
        return "zona"
    elif 10 < x < 18 and y > 10:
        return "zona"
    elif y >= 5 and y <= 10 and 10 < x < 18:
        return "zona central"
    elif y < 7:
        return "media distancia izquierda"
    elif y > 8:
        return "media distancia derecha"
    else:
        return "perímetro"

def fusionar_datos_con_acciones(df_fisicos, df_etiquetas):
    df_fisicos = df_fisicos.copy()
    df_fisicos["tipo"] = None
    df_fisicos["accion"] = None
    df_fisicos["zona"] = None
    df_fisicos["resultado"] = None
    df_fisicos["jugadores_en_accion"] = 0
    df_fisicos["zona_gps"] = df_fisicos.apply(lambda row: determinar_zona_gps(row["x_pos"], row["y_pos"]), axis=1)

    # Para eficiencia, ordenamos las etiquetas por inicio
    df_etiquetas = df_etiquetas.sort_values("inicio")

    for _, row in df_etiquetas.iterrows():
        mask = (
            (df_fisicos["jugador"] == row["jugador"]) &
            (df_fisicos["tiempo"] >= row["inicio"]) &
            (df_fisicos["tiempo"] <= row["fin"])
        )
        df_fisicos.loc[mask, "tipo"] = row["tipo"]
        df_fisicos.loc[mask, "accion"] = row["accion"]
        df_fisicos.loc[mask, "zona"] = row["zona"]
        df_fisicos.loc[mask, "resultado"] = row["resultado"]

    # Añadir número de jugadores en cada instante de tiempo (acción simultánea)
    tiempo_jugador_accion = df_fisicos.dropna(subset=["accion"])[["tiempo", "jugador"]]
    conteo = tiempo_jugador_accion.groupby("tiempo").size().reset_index(name="jugadores_en_accion")
    df_fisicos = df_fisicos.merge(conteo, on="tiempo", how="left", suffixes=("", "_conteo"))
    df_fisicos["jugadores_en_accion"] = df_fisicos["jugadores_en_accion_conteo"].fillna(0).astype(int)
    df_fisicos.drop(columns=["jugadores_en_accion_conteo"], inplace=True)

    # Filtrar solo frames con contexto táctico definido
    df_etiquetado = df_fisicos.dropna(subset=["accion", "tipo", "zona"])
    return df_etiquetado
