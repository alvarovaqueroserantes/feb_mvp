"""Compute extra physical KPIs from positions CSV."""

import pandas as pd
import numpy as np
from pathlib import Path

def load_positions(csv_path):
    return pd.read_csv(csv_path)

def compute_kpis(df):
    df = df.copy()
    df.sort_values(["player_id", "frame"], inplace=True)

    FPS = int(round(1 / df["time_s"].diff().median()))

    df["speed_rolling"] = (
        df.groupby("player_id")["speed_mps"]
          .rolling(FPS).mean()
          .reset_index(level=0, drop=True)
    )
    df["acc_rolling"] = (
        df.groupby("player_id")["acc_mps2"]
          .rolling(FPS).mean()
          .reset_index(level=0, drop=True)
    )

    df["player_load"] = df["acc_mps2"].abs() * 0.1
    return df

if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parent.parent / "data"
    df = load_positions(data_dir / "simulated_positions.csv")
    df = compute_kpis(df)
    df.to_csv(data_dir / "positions_with_kpis.csv", index=False)
    print("✔ positions_with_kpis.csv saved.")
