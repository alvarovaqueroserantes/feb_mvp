"""Basic tactical metrics: spacing & Voronoi area."""

import pandas as pd
import numpy as np
from scipy.spatial import Voronoi
from itertools import combinations
from pathlib import Path

COURT_LENGTH = 14  # m
COURT_WIDTH = 15   # m

def spacing_per_frame(df):
    records = []
    for frame, grp in df.groupby("frame"):
        pts = grp[["x_m", "y_m"]].values
        dists = [np.linalg.norm(pts[i] - pts[j]) for i, j in combinations(range(len(pts)), 2)]
        records.append((frame, np.mean(dists)))
    return pd.DataFrame(records, columns=["frame", "spacing_avg_m"])

def voronoi_areas(df):
    out = []
    for frame, grp in df.groupby("frame"):
        pts = grp[["x_m", "y_m"]].values
        vor = Voronoi(pts)
        for pid, reg_idx in zip(grp["player_id"], vor.point_region):
            verts_idx = vor.regions[reg_idx]
            if -1 in verts_idx or len(verts_idx) == 0:
                area = np.nan
            else:
                poly = vor.vertices[verts_idx]
                poly[:, 0] = np.clip(poly[:, 0], 0, COURT_LENGTH)
                poly[:, 1] = np.clip(poly[:, 1], 0, COURT_WIDTH)
                area = 0.5 * abs(np.dot(poly[:, 0], np.roll(poly[:, 1], 1)) -
                                 np.dot(poly[:, 1], np.roll(poly[:, 0], 1)))
            out.append((frame, pid, area))
    return pd.DataFrame(out, columns=["frame", "player_id", "voronoi_m2"])

if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parent.parent / "data"
    df = pd.read_csv(data_dir / "simulated_positions.csv")
    spacing = spacing_per_frame(df)
    vor = voronoi_areas(df)
    spacing.to_csv(data_dir / "spacing_per_frame.csv", index=False)
    vor.to_csv(data_dir / "voronoi_per_frame.csv", index=False)
    print("✔ tactical metrics saved")
