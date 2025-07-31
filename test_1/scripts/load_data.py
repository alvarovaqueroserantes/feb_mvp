# load_data.py (mejorado para robustez y control de errores)
import pandas as pd
import os

def cargar_datos_fisicos(path="data/datos_fisicos_realistas.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo de datos físicos en la ruta: {path}")
    df = pd.read_csv(path)
    columnas_esperadas = {"jugador", "posicion", "tiempo", "hr", "velocidad", "aceleracion", "playerload", "x_pos", "y_pos"}
    if not columnas_esperadas.issubset(df.columns):
        raise ValueError(f"Faltan columnas necesarias en el CSV: {columnas_esperadas - set(df.columns)}")
    return df

def cargar_etiquetas_tacticas(path="data/etiquetas_tacticas_realistas.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo de etiquetas tácticas en la ruta: {path}")
    df = pd.read_csv(path)
    columnas_esperadas = {"jugador", "tipo", "accion", "zona", "inicio", "fin", "resultado"}
    if not columnas_esperadas.issubset(df.columns):
        raise ValueError(f"Faltan columnas necesarias en el CSV: {columnas_esperadas - set(df.columns)}")
    return df