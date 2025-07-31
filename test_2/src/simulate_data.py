"""
Simula una jugada 5×0 REALISTA:
1) PG (1) lleva balón en top
2) Mano-a-mano con SF (3)
3) P&R central con C (5) que sube a bloquear
4) 3 penetra, pasa al roll (5)
5) 5 asiste a SG (2) en la esquina para triple

Se generan:
* positions.csv     — coordenadas jugadores (25 fps, 10 s)
* ball.csv          — trayectoria del balón (poseído por jugador)
* metrics.csv       — KPIs físicos por jugador
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy.interpolate import interp1d

# --------------------------- parámetros globales --------------------------- #
FPS = 25
DUR = 10.0
FRAMES = np.arange(0, DUR, 1 / FPS)

PLAYERS = [1, 2, 3, 4, 5]          # ids
BALL_COLOR = "#ff7f0e"             # naranja

# Key-frames (t, x, y) para cada jugador
key_pts = {
    # t,  x,   y
    1: [(0,  6, 7.5),          # PG top
        (2,  6, 7.5),          # mano-a-mano
        (4,  4, 13),           # se abre a 45°
        (10, 4, 13)],
    2: [(0,  0.8, 14.0),       # SG esquina derecha
        (10, 0.8, 14.0)],
    3: [(0,  4,  2),           # SF ala izquierda
        (2,  5.8, 7.5),        # recibe mano-a-mano
        (4,  5.8, 7.5),        # espera bloqueo
        (6,  1.8, 7.5),        # penetra
        (10, 1.8, 5.0)],
    4: [(0,  4,  12.5),        # PF ala derecha
        (10, 4, 12.5)],
    5: [(0,  1.8, 3.5),        # C poste bajo opuesto
        (4,  5.8, 7.5),        # sube a bloquear
        (6,  2.2, 7.5),        # roll al aro
        (7,  2.2, 7.0),
        (10, 2.2, 7.0)],
}

# Posesión del balón (t, carrier_id)
ball_states = [
    (0, 1),
    (2, 3),
    (6, 5),
    (7, 2),
    (10, 2),
]

# ----------------------------- helpers ------------------------------------ #
def interpolate_path(points):
    """Devuelve funciones x(t), y(t) interpoladas linealmente."""
    t, x, y = zip(*points)
    fx = interp1d(t, x, kind="linear")
    fy = interp1d(t, y, kind="linear")
    return fx, fy


def build_positions():
    rows = []
    for pid in PLAYERS:
        fx, fy = interpolate_path(key_pts[pid])
        for t in FRAMES:
            rows.append((t, pid, float(fx(t)), float(fy(t))))
    pos = pd.DataFrame(rows, columns=["time", "player_id", "x_m", "y_m"])
    pos["frame"] = (pos["time"] * FPS).round().astype(int)
    pos.sort_values(["player_id", "frame"], inplace=True)
    return pos


def build_ball(pos_df):
    # Interpola coordenadas del balón a partir del portador
    carrier_series = pd.Series(index=FRAMES)
    for t, pid in ball_states:
        carrier_series.loc[t] = pid
    carrier_series.ffill(inplace=True)

    ball_rows = []
    for t in FRAMES:
        pid = int(carrier_series.loc[t])
        row = pos_df[(pos_df.player_id == pid) & (np.isclose(pos_df.time, t))].iloc[0]
        ball_rows.append((t, row["x_m"], row["y_m"]))
    ball = pd.DataFrame(ball_rows, columns=["time", "x_m", "y_m"])
    ball["frame"] = (ball["time"] * FPS).round().astype(int)
    return ball


def physical_metrics(df):
    df = df.copy()
    df[["vx", "vy"]] = df.groupby("player_id")[["x_m", "y_m"]].diff() * FPS
    df["speed"] = np.linalg.norm(df[["vx", "vy"]], axis=1)
    df["acc"] = df.groupby("player_id")["speed"].diff() * FPS
    step = df.groupby("player_id")[["x_m", "y_m"]].diff()
    df["step_dist"] = np.sqrt(step["x_m"] ** 2 + step["y_m"] ** 2).fillna(0)
    return (
        df.groupby("player_id")
          .agg(total_dist_m=("step_dist", "sum"),
               max_speed=("speed", "max"),
               mean_speed=("speed", "mean"))
          .reset_index()
    )


# ----------------------------- main --------------------------------------- #
if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    pos = build_positions()
    ball = build_ball(pos)
    metrics = physical_metrics(pos)

    pos.to_csv(data_dir / "positions.csv", index=False)
    ball.to_csv(data_dir / "ball.csv", index=False)
    metrics.to_csv(data_dir / "metrics.csv", index=False)
    print("✔ Datos generados en", data_dir)
