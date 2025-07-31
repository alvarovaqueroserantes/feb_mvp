# analytics.py (versión mejorada con análisis táctico + físico + colectivo)

import pandas as pd

# 1. Cálculo de métricas físicas avanzadas por contexto táctico

def calcular_metricas_avanzadas(df):
    metricas = df.groupby(["jugador", "posicion", "tipo", "accion", "zona"]).agg({
        "hr": ["mean", "max"],
        "velocidad": ["mean", "max"],
        "aceleracion": "mean",
        "playerload": "mean",
        "x_pos": "mean",
        "y_pos": "mean",
        "tiempo": "count"
    })
    metricas.columns = ['_'.join(col).strip() for col in metricas.columns.values]
    metricas = metricas.reset_index()
    return metricas

# 2. Tasa de éxito ofensivo/defensivo por jugador

def calcular_tasa_exito_por_jugador(df_etiquetas):
    df = df_etiquetas.copy()
    df["exito_num"] = (df["resultado"] == "Exito").astype(int)
    tasas = df.groupby(["jugador", "tipo"])["exito_num"].mean().reset_index()
    tasas_pivot = tasas.pivot(index="jugador", columns="tipo", values="exito_num").fillna(0)
    tasas_pivot = tasas_pivot.rename(columns={
        "ataque": "tasa_exito_ofensivo",
        "defensa": "tasa_exito_defensivo"
    }).reset_index()
    return tasas_pivot

# 3. Detección de combinaciones tácticas ofensivas

def detectar_combinaciones(df_etiquetas):
    combinaciones = []
    eventos = df_etiquetas[df_etiquetas["tipo"] == "ataque"].to_dict('records')
    for i, ev1 in enumerate(eventos):
        for j in range(i+1, len(eventos)):
            ev2 = eventos[j]
            if ev1["jugador"] != ev2["jugador"] and not (ev1["fin"] < ev2["inicio"] or ev1["inicio"] > ev2["fin"]):
                acciones = {ev1["accion"], ev2["accion"]}
                if "bloqueo directo (sin balón)" in acciones and "corte" in acciones:
                    screener, cutter = (ev1, ev2) if ev1["accion"].startswith("bloqueo") else (ev2, ev1)
                    combinaciones.append({
                        "jugador_1": screener["jugador"], "accion_1": screener["accion"],
                        "jugador_2": cutter["jugador"], "accion_2": cutter["accion"],
                        "resultado": cutter["resultado"]
                    })
                if "bloqueo directo (con balón)" in acciones:
                    if "penetración" in acciones:
                        screener, ballhandler = (ev1, ev2) if ev1["accion"].startswith("bloqueo") else (ev2, ev1)
                        combinaciones.append({
                            "jugador_1": screener["jugador"], "accion_1": screener["accion"],
                            "jugador_2": ballhandler["jugador"], "accion_2": ballhandler["accion"],
                            "resultado": ballhandler["resultado"]
                        })
                    elif "tiro" in acciones:
                        screener, shooter = (ev1, ev2) if ev1["accion"].startswith("bloqueo") else (ev2, ev1)
                        combinaciones.append({
                            "jugador_1": screener["jugador"], "accion_1": screener["accion"],
                            "jugador_2": shooter["jugador"], "accion_2": shooter["accion"],
                            "resultado": shooter["resultado"]
                        })
    return pd.DataFrame(combinaciones).drop_duplicates()

# 4. Análisis de fatiga basado en evolución HR + velocidad

def detectar_fatiga(df_fisicos):
    resultados = []
    for jugador, datos in df_fisicos.groupby("jugador"):
        tiempo_total = datos["tiempo"].max()
        inicio = datos[datos["tiempo"] < 120]
        final = datos[datos["tiempo"] > (tiempo_total - 120)]
        if len(inicio) == 0 or len(final) == 0:
            continue
        vel_ini = inicio["velocidad"].mean()
        vel_fin = final["velocidad"].mean()
        hr_ini = inicio["hr"].mean()
        hr_fin = final["hr"].mean()
        fatiga_flag = (vel_fin < 0.9 * vel_ini) and (hr_fin > hr_ini + 5)
        resultados.append({
            "jugador": jugador,
            "velocidad_inicial": vel_ini,
            "velocidad_final": vel_fin,
            "hr_inicial": hr_ini,
            "hr_final": hr_fin,
            "fatiga": fatiga_flag
        })
    return pd.DataFrame(resultados)

# 5. Cruce físico-táctico por resultado (exito/fallo)

def resumen_fisico_vs_resultado(df):
    resumen = df.groupby("resultado")[["playerload", "velocidad", "hr"]].mean().reset_index()
    resumen.columns = ["tipo_resultado", "playerload", "velocidad", "hr"]
    return resumen
